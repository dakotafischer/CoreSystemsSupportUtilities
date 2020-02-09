from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from lxml import etree as ET
from signxml import XMLSigner, XMLVerifier
import signxml
import datetime
from datetime import timedelta
import base64

import xml.dom.minidom

'''
Note: BF has Internet Explorer locked down on the RDP's where you could otherwise test legacy IE issues
The main issue is that it blocks csrf tokens so to make this app usable on those virtual desktops, make the following
imports and add the csrf_exempt decorator to the SamlPostView

from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 

@method_decorator(csrf_exempt, name='dispatch')
'''


class SamlPostView(generic.ListView):
    '''A view that processes input from a user and returns a signed SAML Response'''

    template_name = 'saml_post/saml_post.html'
    context_object_name = 'query_set'
    fields = {'issuer_id': 'SAML_Post.Test_Entity_ID',
              'saml_subject': 'some-example-id',
              'attribute_name': 'SSO_ID',
              'attribute_value': '46379',
              'audience_id': 'benefitfocus.com:sp',
              'acs_endpoint': 'https://secure-enroll.com/sso/saml', }

    def get_queryset(self, request, *args, **kwargs):
        return render(request, self.template_name, {'fields': self.fields})

    def get(self, request, *args, **kwargs):
        '''GET requests reset the fields to their default values and render the form.'''
        self.fields = {'issuer_id': 'SAML_Post.Test_Entity_ID',
                        'saml_subject': 'some-example-id',
                        'attribute_name': 'SSO_ID',
                        'attribute_value': '46379',
                        'audience_id': 'benefitfocus.com:sp',
                        'acs_endpoint': 'https://secure-enroll.com/sso/saml', }
        return render(request, self.template_name, {'fields': self.fields})

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        self.update_default_fields(post_data)
        signed_saml = self.generate_saml(post_data)
        encoded_saml = base64.b64encode(signed_saml)
        encoding = 'utf-8'
        encoded_saml = encoded_saml.decode('utf-8')
        signed_saml = xml.dom.minidom.parseString(signed_saml).toprettyxml()
        return render(request, self.template_name,
                      {'signed_saml': signed_saml, 'encoded_saml': encoded_saml, 'fields': self.fields})
                     # {'signed_saml': signed_saml.decode('utf-8'), 'encoded_saml': encoded_saml, 'fields': self.fields})

    def generate_saml(self, post_data):
        '''Update all of the relevant fields in saml_template.xml with the form data'''
        parser = ET.XMLParser(remove_blank_text=True)
        now = datetime.datetime.utcnow()
        issue_instant = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'
        tree = ET.parse('saml_post/static/saml_post/saml_template.xml', parser=parser)
        # if this ever breaks it might be easier to troubleshoot with the template as a string
        ## saml_template = '<samlp:Response ID="_4ba3eca7-7f9f-4a77-9006-4e1fae8bee1b" Version="2.0" IssueInstant="2020-01-10T13:09:52.256Z" Destination="https://secure-enroll.com/sso/saml" xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"><Issuer xmlns="urn:oasis:names:tc:SAML:2.0:assertion">https://sts.windows.net/23e14383-b783-4c99-bf4f-5049cd014ec6/</Issuer><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Id="placeholder" /><samlp:Status><samlp:StatusCode Value="urn:oasis:names:tc:SAML:2.0:status:Success"/></samlp:Status><Assertion ID="_fdaa4a4b-ffad-4d60-bb95-86bb6c312000" IssueInstant="2020-01-10T13:09:52.256Z" Version="2.0" xmlns="urn:oasis:names:tc:SAML:2.0:assertion"><Issuer>https://sts.windows.net/23e14383-b783-4c99-bf4f-5049cd014ec6/</Issuer><Subject><NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient">0VFMNdkRdozsmj7W8PDmoCgje2almNSSeKSz1N2v1FM</NameID><SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer"><SubjectConfirmationData NotOnOrAfter="2020-01-10T14:09:51.974Z" Recipient="https://secure-enroll.com/sso/saml"/></SubjectConfirmation></Subject><Conditions NotBefore="2020-01-10T13:04:51.974Z" NotOnOrAfter="2020-01-10T14:09:51.974Z"><AudienceRestriction><Audience>https://secure-enroll.com/sso/saml</Audience></AudienceRestriction></Conditions><AttributeStatement><Attribute Name="http://schemas.microsoft.com/identity/claims/tenantid"><AttributeValue>23e14383-b783-4c99-bf4f-5049cd014ec6</AttributeValue></Attribute></AttributeStatement></Assertion></samlp:Response>'
        ## root = ET.fromstring(saml_template)
        root = tree.getroot()
        # namespaces are ew but you can use .find('saml:Assertion', saml) where the second parameter (saml) is this dictionary instead of indexing into each element
        saml = {'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
                'signature': 'http://www.w3.org/2000/09/xmldsig#}Signature'}
        root.find('saml:Issuer', saml).text = post_data['issuer_id']
        root.attrib['Destination'] = post_data['acs_endpoint']
        root.attrib['IssueInstant'] = issue_instant
        root.find('saml:Assertion', saml).attrib['IssueInstant'] = issue_instant
        root.find('saml:Assertion', saml).find('saml:Subject', saml).find('saml:NameID', saml).text = post_data[
            'saml_subject']
        root.find('saml:Assertion', saml).find('saml:Subject', saml).find('saml:SubjectConfirmation', saml).find(
            'saml:SubjectConfirmationData', saml).attrib['NotOnOrAfter'] = (now + timedelta(hours=1)).strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'
        root.find('saml:Assertion', saml).find('saml:Subject', saml).find('saml:SubjectConfirmation', saml).find(
            'saml:SubjectConfirmationData', saml).attrib['Recipient'] = post_data['audience_id']
        root.find('saml:Assertion', saml).find('saml:Conditions', saml).attrib['NotBefore'] = (now - timedelta(
            minutes=10)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'
        root.find('saml:Assertion', saml).find('saml:Conditions', saml).attrib['NotOnOrAfter'] = (now + timedelta(
            hours=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'
        root.find('saml:Assertion', saml).find('saml:Conditions', saml).find('saml:AudienceRestriction', saml).find(
            'saml:Audience', saml).text = post_data['audience_id']
        root.find('saml:Assertion', saml).find('saml:AttributeStatement', saml).find('saml:Attribute', saml).attrib[
            'Name'] = post_data['attribute_name']
        root.find('saml:Assertion', saml).find('saml:AttributeStatement', saml).find('saml:Attribute', saml).find(
            'saml:AttributeValue', saml).text = post_data['attribute_value']
        root.find('saml:Assertion', saml).find('saml:Issuer', saml).text = post_data['issuer_id']

        # sign the newly created xml
        reference_uri = '_4ba3eca7-7f9f-4a77-9006-4e1fae8bee1b'
        with open("saml_post/static/saml_post/publickey.cer") as f:
            cert = f.read()
        with open("saml_post/static/saml_post/private.key") as f:
            key = f.read()
        '''
        From the SAML Oasis docs:
        Signatures in SAML messages SHOULD NOT contain transforms other than the enveloped signature transform 
        (with the identifier http://www.w3.org/2000/09/xmldsig#enveloped-signature) 
        or the exclusive canonicalization transforms 
        (with the identifier http://www.w3.org/2001/10/xml-exc-c14n# 
        or http://www.w3.org/2001/10/xml-exc-c14n#WithComments).
        The default behavior for XMLSigner uses some other transforms so we need to specify the c14n_algorithm.
        '''
        signer = XMLSigner(c14n_algorithm='http://www.w3.org/2001/10/xml-exc-c14n#', signature_algorithm="rsa-sha256",
                           digest_algorithm="sha256", method=signxml.methods.enveloped)
        signed_root = signer.sign(root, key=key, cert=cert, reference_uri=reference_uri)
        return ET.tostring(signed_root, encoding='utf-8')

    def update_default_fields(self, post_data):
        self.fields['issuer_id'] = post_data['issuer_id']
        self.fields['saml_subject'] = post_data['saml_subject']
        self.fields['attribute_name'] = post_data['attribute_name']
        self.fields['attribute_value'] = post_data['attribute_value']
        self.fields['audience_id'] = post_data['audience_id']
        self.fields['acs_endpoint'] = post_data['acs_endpoint']
        return None

