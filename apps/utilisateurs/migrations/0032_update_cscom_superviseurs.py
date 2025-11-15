# Generated manually

from django.db import migrations


def update_cscom_superviseurs(apps, schema_editor):
    """Met à jour les CSCom-U avec les informations des CEC/Superviseurs Principaux"""
    CSComUCentre = apps.get_model('utilisateurs', 'CSComUCentre')
    
    # Mapping des codes CSCom vers les superviseurs
    superviseurs_par_code = {
        'CSCOM-U-KONONBOUGOU': 'Mamadou Bayo COULIBALY',
        'CSCOM-U-BANCONI': 'Drissa Mansa SIDIBE',
        'CSCOM-U-SANOUBOUGOU-2': 'Kafoungo COULIBALY',
        'CSCOM-U-SANAKOROBA': 'Kany KEÏTA',
        'CSCOM-U-SEGUE': 'Bintou DOUMBIA',
        'CSCOM-U-KAYES-NDI': 'Binta S SIDIEBE',
        'CSCOM-U-KONIAKARY': '',  # Pas de superviseur car pas de Médecin de Famille
    }
    
    # Mettre à jour les superviseurs
    for code, superviseur in superviseurs_par_code.items():
        try:
            cscom = CSComUCentre.objects.get(code=code)
            cscom.cec_superviseur_principal = superviseur
            # Koniakary ne reçoit pas d'étudiants
            if code == 'CSCOM-U-KONIAKARY':
                cscom.actif = False
            cscom.save()
        except CSComUCentre.DoesNotExist:
            # Le CSCom n'existe pas encore, on continue
            pass


def reverse_update_cscom_superviseurs(apps, schema_editor):
    """Annule les mises à jour des superviseurs"""
    CSComUCentre = apps.get_model('utilisateurs', 'CSComUCentre')
    
    codes_a_reinitialiser = [
        'CSCOM-U-KONONBOUGOU',
        'CSCOM-U-BANCONI',
        'CSCOM-U-SANOUBOUGOU-2',
        'CSCOM-U-SANAKOROBA',
        'CSCOM-U-SEGUE',
        'CSCOM-U-KAYES-NDI',
        'CSCOM-U-KONIAKARY',
    ]
    
    for code in codes_a_reinitialiser:
        try:
            cscom = CSComUCentre.objects.get(code=code)
            cscom.cec_superviseur_principal = ''
            if code == 'CSCOM-U-KONIAKARY':
                cscom.actif = True
            cscom.save()
        except CSComUCentre.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0031_cscomucentre_cec_superviseur_principal'),
    ]

    operations = [
        migrations.RunPython(update_cscom_superviseurs, reverse_update_cscom_superviseurs),
    ]

