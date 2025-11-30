# apps/evaluations/utils_pdf.py
"""
Utilitaires pour la génération de PDF des évaluations de stage
"""
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from .models_stage import EvaluationStage, EvaluationJalonStage
from apps.utilisateurs.models_formation import Classe, CompetenceJalon


def generate_evaluation_stage_pdf(evaluation):
    """Génère un PDF pour une évaluation de stage remplie"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # En-tête
    story.append(Paragraph("ÉVALUATION DE STAGE", title_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Informations générales
    info_data = [
        ['Étudiant:', f"{evaluation.etudiant.get_full_name() or evaluation.etudiant.username}"],
        ['Classe:', evaluation.classe.nom],
        ['Structure de stage:', evaluation.get_structure_display()],
        ['Superviseur:', evaluation.get_superviseur_display()],
        ['Type d\'évaluation:', evaluation.get_type_evaluation_display()],
        ['Date:', evaluation.date_evaluation.strftime('%d/%m/%Y')],
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 1*cm))
    
    # Organiser les jalons par compétence
    evaluations_jalons = evaluation.evaluations_jalons.select_related(
        'jalon', 'jalon__competence'
    ).order_by('jalon__competence__libelle', 'jalon__ordre', 'ordre')
    
    competences_data = {}
    for eval_jalon in evaluations_jalons:
        competence = eval_jalon.jalon.competence
        if competence not in competences_data:
            competences_data[competence] = []
        competences_data[competence].append(eval_jalon)
    
    # Tableau des évaluations par compétence
    for competence, eval_jalons in competences_data.items():
        # Titre de la compétence
        story.append(Paragraph(
            f"<b>{competence.get_domaine_display()}: {competence.libelle}</b>",
            styles['Heading2']
        ))
        story.append(Spacer(1, 0.3*cm))
        
        # Tableau des jalons
        table_data = [['Jalon', 'Niveau', 'Commentaire']]
        
        for eval_jalon in eval_jalons:
            niveau_display = eval_jalon.get_niveau_display() if eval_jalon.niveau else 'Non évalué'
            commentaire = eval_jalon.commentaire or ''
            table_data.append([
                eval_jalon.jalon.titre,
                niveau_display,
                commentaire[:100] + '...' if len(commentaire) > 100 else commentaire
            ])
        
        jalon_table = Table(table_data, colWidths=[7*cm, 3*cm, 6*cm])
        jalon_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(jalon_table)
        story.append(Spacer(1, 0.5*cm))
    
    # Commentaire général
    if evaluation.commentaire_general:
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("<b>Commentaire général:</b>", styles['Heading3']))
        story.append(Paragraph(evaluation.commentaire_general, styles['Normal']))
        story.append(Spacer(1, 0.5*cm))
    
    # Signature et cachet
    story.append(Spacer(1, 1*cm))
    signature_data = [
        ['Signature du responsable:', 'Cachet de la structure:'],
    ]
    signature_table = Table(signature_data, colWidths=[9*cm, 7*cm])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(signature_table)
    
    # Construire le PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_blank_evaluation_stage_pdf(classe):
    """Génère un PDF vierge pour une grille d'évaluation de stage"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # En-tête
    story.append(Paragraph("GRILLE D'ÉVALUATION DE STAGE", title_style))
    story.append(Paragraph(f"Classe: {classe.nom}", styles['Heading2']))
    story.append(Spacer(1, 0.5*cm))
    
    # Informations générales (vierges)
    info_data = [
        ['Étudiant:', ''],
        ['Classe:', classe.nom],
        ['Structure de stage:', ''],
        ['Superviseur:', ''],
        ['Type d\'évaluation:', ''],
        ['Date:', ''],
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 12*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 1*cm))
    
    # Récupérer les jalons de la classe
    jalons = CompetenceJalon.objects.filter(
        classe=classe,
        actif=True
    ).select_related('competence').order_by('competence__libelle', 'ordre', 'titre')
    
    # Organiser par compétence
    competences_data = {}
    for jalon in jalons:
        competence = jalon.competence
        if competence not in competences_data:
            competences_data[competence] = []
        competences_data[competence].append(jalon)
    
    # Tableau vierge des évaluations par compétence
    for competence, jalons_list in competences_data.items():
        # Titre de la compétence
        story.append(Paragraph(
            f"<b>{competence.get_domaine_display()}: {competence.libelle}</b>",
            styles['Heading2']
        ))
        story.append(Spacer(1, 0.3*cm))
        
        # Tableau vierge des jalons
        table_data = [['Jalon', 'Niveau', 'Commentaire']]
        
        for jalon in jalons_list:
            table_data.append([
                jalon.titre,
                '',
                ''
            ])
        
        jalon_table = Table(table_data, colWidths=[7*cm, 3*cm, 6*cm])
        jalon_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(jalon_table)
        story.append(Spacer(1, 0.5*cm))
    
    # Commentaire général (vierge)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>Commentaire général:</b>", styles['Heading3']))
    story.append(Spacer(1, 2*cm))
    story.append(Spacer(1, 0.5*cm))
    
    # Signature et cachet (vierges)
    story.append(Spacer(1, 1*cm))
    signature_data = [
        ['Signature du responsable:', 'Cachet de la structure:'],
    ]
    signature_table = Table(signature_data, colWidths=[9*cm, 7*cm])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(signature_table)
    
    # Construire le PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

