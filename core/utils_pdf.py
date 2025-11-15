# core/utils_pdf.py
"""
Utilitaires pour la génération de PDFs
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from django.conf import settings
import os
import re


def generate_pdf_response(html_content, filename, css_content=None):
    """
    Génère une réponse HTTP avec un PDF
    
    Args:
        html_content: Contenu HTML à convertir en PDF
        filename: Nom du fichier PDF
        css_content: CSS optionnel pour le style
    
    Returns:
        HttpResponse avec le PDF
    """
    # CSS par défaut pour l'impression
    default_css = """
    @page {
        size: A4;
        margin: 2cm;
    }
    body {
        font-family: Arial, sans-serif;
        font-size: 12pt;
        line-height: 1.6;
    }
    h1 {
        color: #005a9c;
        font-size: 24pt;
        margin-bottom: 20px;
    }
    h2 {
        color: #005a9c;
        font-size: 18pt;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #005a9c;
        color: white;
        font-weight: bold;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 2px solid #005a9c;
        padding-bottom: 15px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
        font-size: 10pt;
        color: #666;
    }
    .signature-section {
        margin-top: 50px;
        padding-top: 30px;
        border-top: 2px solid #005a9c;
        text-align: right;
    }
    .signature-content {
        display: inline-block;
        text-align: center;
        min-width: 300px;
    }
    .cachet-image {
        max-width: 150px;
        max-height: 150px;
        margin-bottom: 10px;
    }
    .signature-name {
        font-weight: bold;
        font-size: 12pt;
        margin-top: 20px;
        margin-bottom: 5px;
    }
    .signature-title {
        font-size: 10pt;
        color: #666;
        margin-bottom: 10px;
    }
    """
    
    # Combiner les CSS dans le HTML
    if css_content:
        combined_css = default_css + "\n" + css_content
    else:
        combined_css = default_css
    
    # Convertir les URLs relatives des images en chemins absolus pour xhtml2pdf
    def convert_image_url(match):
        url = match.group(1)
        # Si c'est déjà une URL absolue ou file://, la laisser telle quelle
        if url.startswith('http://') or url.startswith('https://') or url.startswith('file://'):
            return match.group(0)
        # Si c'est une URL media Django, la convertir en chemin absolu
        if url.startswith('/media/'):
            # Pour xhtml2pdf, utiliser le chemin du système de fichiers
            media_path = os.path.join(settings.MEDIA_ROOT, url.replace('/media/', ''))
            if os.path.exists(media_path):
                # Convertir en chemin absolu Windows/Linux compatible
                abs_path = os.path.abspath(media_path)
                # Normaliser les séparateurs pour file://
                file_url = abs_path.replace('\\', '/')
                if not file_url.startswith('/'):
                    file_url = '/' + file_url
                return f'src="file://{file_url}"'
        return match.group(0)
    
    # Remplacer les src d'images dans le HTML
    html_content = re.sub(r'src="([^"]+)"', convert_image_url, html_content)
    
    # Ajouter le CSS dans le HTML
    # Vérifier si le HTML contient déjà une structure complète
    if '<html' in html_content.lower() or '<!doctype' in html_content.lower():
        # Le HTML est déjà complet, ajouter le CSS dans le <head>
        if '<head>' in html_content.lower():
            html_with_css = html_content.replace(
                '</head>',
                f'<style>{combined_css}</style></head>',
                1
            )
        elif '<style>' in html_content.lower():
            # Ajouter avant le premier </style>
            html_with_css = html_content.replace(
                '</style>',
                f'{combined_css}</style>',
                1
            )
        else:
            # Ajouter après <head> ou avant <body>
            if '<head>' in html_content.lower():
                html_with_css = html_content.replace(
                    '<head>',
                    f'<head><style>{combined_css}</style>',
                    1
                )
            elif '<body>' in html_content.lower():
                html_with_css = html_content.replace(
                    '<body>',
                    f'<head><style>{combined_css}</style></head><body>',
                    1
                )
            else:
                html_with_css = f'<style>{combined_css}</style>{html_content}'
    else:
        # Le HTML n'est pas complet, créer une structure complète
        html_with_css = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
    {combined_css}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
    
    # Générer le PDF avec xhtml2pdf
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html_with_css.encode("UTF-8")), result)
    
    if pdf.err:
        raise Exception(f"Erreur lors de la génération du PDF: {pdf.err}")
    
    # Créer la réponse HTTP
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


def generate_pdf_from_template(template_name, context, filename, css_template=None):
    """
    Génère un PDF à partir d'un template Django
    
    Args:
        template_name: Nom du template HTML
        context: Contexte pour le template
        filename: Nom du fichier PDF
        css_template: Template CSS optionnel
    
    Returns:
        HttpResponse avec le PDF
    """
    # Ajouter les informations de signature de la coordination au contexte
    from apps.utilisateurs.models_documents import SignatureCoordination
    signature = SignatureCoordination.get_signature_active()
    if signature:
        context['signature_coordination'] = signature
    
    # Rendre le template HTML
    html_content = render_to_string(template_name, context)
    
    # Rendre le CSS si fourni
    css_content = None
    if css_template:
        css_content = render_to_string(css_template, context)
    
    return generate_pdf_response(html_content, filename, css_content)


def send_pdf_by_email(pdf_content, filename, subject, message, recipient_email, from_email=None):
    """
    Envoie un PDF par email
    
    Args:
        pdf_content: Contenu binaire du PDF
        filename: Nom du fichier PDF
        subject: Sujet de l'email
        message: Message de l'email
        recipient_email: Email du destinataire
        from_email: Email expéditeur (optionnel)
    
    Returns:
        True si l'email a été envoyé avec succès
    """
    from django.core.mail import EmailMessage
    from django.conf import settings
    
    if not from_email:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@fmos-mfmc.ml')
    
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[recipient_email],
        )
        email.attach(filename, pdf_content, 'application/pdf')
        email.send()
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False

