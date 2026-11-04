"""Initial construction only. Maintain the JSON files after this release."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-11-03'
sources=[]
terms=[]
indicators=[]

def source(id,publisher,title,url,access='full_page'):
    sources.append(dict(id=id,publisher=publisher,title=title,url=url,checked_at=DATE,evidence_access=access))

source('fbi-nve','FBI Boston','Nihilistic Violent Extremists Targeting Children and Vulnerable Victims Online','https://www.fbi.gov/contact-us/field-offices/boston/news/fbi-boston-warns-of-nihilistic-violent-extremists-targeting-children-and-vulnerable-victims-online')
source('ctc-nve','Combating Terrorism Center at West Point','Remotely Coerced Violence: 764, The Com Network, and the Hybridization of Threats','https://ctc.westpoint.edu/remotely-coerced-violence-764-the-com-network-and-the-hybridization-of-threats/')
source('fbi-prevention','Federal Bureau of Investigation','Making Prevention a Reality (2017)','https://www.fbi.gov/file-repository/reports-and-publications/making-prevention-a-reality.pdf/download','full_pdf; warning behaviors and pathway discussion')
source('fbi-behavior','Federal Bureau of Investigation','Behavioral Analysis','https://www.fbi.gov/how-we-investigate/behavioral-analysis')
source('fbi-mobilization','NCTC / FBI / DHS','Violent Extremist Mobilization Indicators: Critical Infrastructure Sector','https://www.fbi.gov/file-repository/counterterrorism/us-violent-extremism-mobilization-indicators-critical-infrastructure-sector.pdf','full_pdf; 2021 indicator supplement, not the 2025 booklet')
source('trap-owner','J. Reid Meloy','TRAP-18 Manual overview','https://drreidmeloy.com/training/trap-18/')
source('wavr-owner','WAVR-21 developers','The WAVR-21','https://wavr21.com/wavr-21/')
source('atf','Bureau of Alcohol, Tobacco, Firearms and Explosives','Suspicious or Dangerous Items','https://www.atf.gov/explosives/tools-services-explosives-industry/current-licensees/suspicious-or-dangerous-items')
source('uk-home-office','UK Home Office','Supplying explosives precursors and poisons','https://www.gov.uk/government/publications/supplying-explosives-precursors/supplying-explosives-precursors-and-poison')
source('au-security','Australian National Security','Industry specific advice for chemical security','https://www.nationalsecurity.gov.au/protect-your-business/chemical-security/industry','search_index_excerpt; transaction details not exposed in full-page fetch')
source('usss-schools','United States Secret Service / NTAC','Protecting America’s Schools (2019)','https://www.secretservice.gov/sites/default/files/2020-04/Protecting_Americas_Schools.pdf','search_index_excerpt from official PDF with query parameters; direct clean URL returned 403')

def term(id,en,de,category,refs,scope='general_targeted_violence',basis='project_query_vocabulary'):
    terms.append(dict(id=id,terms={'en':en,'de':de},category=category,source_ids=refs.split(','),scope=scope,
        evidence_basis=basis,german_basis='project_translation_not_source_attested' if de else 'not_applicable',
        action='human_review',reviewed_at=DATE,status='initial_research',
        context_note='Literal mention only: quotation, reporting, education, prevention, victim disclosure, and benign use require review. No intent or behavior is inferred.'))

term('764',['764'],[],'network_reference','fbi-nve','nve_related','source_attested_label')
term('nlm',['No Lives Matter','NLM'],[],'network_reference','ctc-nve','nve_related','source_attested_label')
term('com',['Com Network'],[],'network_reference','ctc-nve','nve_related','source_attested_label')
term('mmc',['Maniac Murder Cult'],[],'network_reference','ctc-nve','nve_related','source_attested_label')
term('nve',['nihilistic violent extremism','NVE'],['nihilistischer Gewaltextremismus'],'research_reference','fbi-nve','nve_related','source_attested_label')
term('soe',['sadistic online exploitation'],['sadistische Online-Ausbeutung'],'exploitation','fbi-nve','nve_related','source_attested_label')
term('trap',['TRAP-18','TRAP 18','Terrorist Radicalization Assessment Protocol'],[],'framework_reference','trap-owner','framework_only','source_attested_label')
term('wavr',['WAVR-21','WAVR 21','Workplace Assessment of Violence Risk'],[],'framework_reference','wavr-owner','framework_only','source_attested_label')
for id,en,de,cat,ref in [
 ('planning','attack planning','Anschlagsplanung','preparation','fbi-prevention'),
 ('preparation','attack preparation','Anschlagsvorbereitung','preparation','fbi-prevention'),
 ('prior-attacks','past attackers','frühere Attentäter','prior_attacker_reference','fbi-mobilization'),
 ('prior-shooters','previous shooters','frühere Amokläufer','prior_attacker_reference','fbi-prevention'),
 ('mass-shootings','mass shootings','Massenschießereien','prior_attacker_reference','fbi-prevention'),
 ('target','target surveillance','Zielausspähung','targeting','fbi-prevention'),
 ('threat','death threat','Morddrohung','threat_reference','fbi-prevention'),
 ('leakage','leakage','Leakage','research_reference','fbi-prevention'),
 ('fixation','fixation','Fixierung','research_reference','trap-owner'),
 ('weapons-access','access to weapons','Zugang zu Waffen','weapons_context','usss-schools'),
 ('weapons-acquisition','weapons acquisition','Waffenbeschaffung','weapons_context','usss-schools'),
 ('coercion','coerced self-harm','erzwungene Selbstverletzung','exploitation','fbi-nve'),
 ('sextortion','sextortion','sexuelle Erpressung','exploitation','fbi-nve'),
 ('doxing','doxing','Doxing','exploitation','fbi-nve'),
 ('swatting','swatting','Swatting','exploitation','fbi-nve'),
 ('animal','animal cruelty','Tierquälerei','exploitation','fbi-nve'),
 ('harm-footage','violent footage','Gewaltaufnahmen','exploitation','ctc-nve'),
 ('explosives','explosives research','Sprengstoffrecherche','explosives_context','fbi-prevention'),
 ('explosive-device','explosive device','Sprengvorrichtung','explosives_context','atf'),
 ('precursor','explosives precursor','Ausgangsstoff für Explosivstoffe','explosives_context','uk-home-office'),
 ('chemical-security','chemical security','Chemikaliensicherheit','explosives_context','au-security'),
 ('suspicious-transaction','suspicious transaction','verdächtige Transaktion','procurement_context','uk-home-office'),
 ('chemical-theft','chemical theft','Chemikaliendiebstahl','procurement_context','uk-home-office'),
 ('chemical-loss','missing chemicals','vermisste Chemikalien','procurement_context','uk-home-office'),
]:
    term(id,[en],[de],cat,ref,'nve_related' if ref in {'fbi-nve','ctc-nve'} else 'general_targeted_violence')
for t in terms:
    if t['id']=='doxing':t['terms']['en'].append('doxxing')

def indicator(id,label,domain,summary,refs,scope='general_targeted_violence',questions=None):
    indicators.append(dict(id=id,label=label,domain=domain,summary=summary,source_ids=refs.split(','),scope=scope,
        evidence_basis='project_authored_observation_prompt',
        evidence_needed=questions or ['What was directly observed, by whom, and when?','What links this to intended harm, rather than a benign explanation?','What changed over time, and what evidence contradicts the concern?'],
        action='human_review',automated_inference=False,reviewed_at=DATE,status='initial_research'))

indicator('research-intent','Research connected to violent intent','preparation','Establish an observed link between research and intended harm.','fbi-prevention')
indicator('attacker-emulation','Past-attacker emulation','identification','Distinguish emulation from historical or journalistic research.','fbi-mobilization')
indicator('preparatory-change','Preparation beyond ordinary activity','preparation','Record changes indicating movement toward an attack.','fbi-prevention')
indicator('communicated-intent','Communication of intended violence','communication','Document threats or disclosures with their surrounding context.','fbi-prevention')
indicator('targeted-attention','Attention focused on a potential target','targeting','Document observed targeting activity and legitimate explanations.','fbi-prevention')
indicator('weapon-access','Access relevant to a threat','weapons_context','Establish actual access separately from claims or images.','usss-schools')
indicator('weapon-acquisition','Acquisition linked to planning','weapons_context','Review acquisition in relation to a documented threat.','usss-schools')
indicator('harm-coercion','Coercion into self-harm','exploitation','Identify coercion and safeguard potential victims.','fbi-nve','nve_related')
indicator('sexual-extortion','Sexual extortion','exploitation','Assess coercion without treating disclosure as culpability.','fbi-nve','nve_related')
indicator('dox-threat','Doxing or swatting intimidation','exploitation','Review use of intimidation to compel harmful acts.','fbi-nve','nve_related')
indicator('animal-harm','Coerced animal harm','exploitation','Distinguish instructions, disclosure, threats, and reporting.','fbi-nve','nve_related')
indicator('harm-status','Violence used for network status','exploitation','Review encouragement or circulation of harm for standing.','ctc-nve','nve_related')
indicator('explosive-intent','Explosives inquiry linked to harm','explosives_context','Review explicit harmful intent alongside research or acquisition.','fbi-prevention,atf')
indicator('purpose-evasion','Unexplained intended use','procurement_context','Document conflicting or withheld purpose in a relevant transaction.','uk-home-office')
indicator('id-evasion','Reluctance to provide required identification','procurement_context','Review identification concerns in context of applicable requirements.','atf')
indicator('quantity-anomaly','Unusual purchasing pattern','procurement_context','Compare observed orders with legitimate needs and prior patterns.','uk-home-office,au-security')
indicator('delivery-anomaly','Unusual delivery or packaging','procurement_context','Review unexplained delivery requests in transaction context.','uk-home-office,au-security')
indicator('inventory-loss','Significant loss or theft','procurement_context','Record missing inventory and corroboration separately from speculation.','uk-home-office')
indicator('restricted-access','Unauthorized access to explosives storage','explosives_context','Document access concerns without confronting or investigating privately.','atf')
indicator('protective-context','Evidence inconsistent with intended harm','protective_context','Record support, de-escalation, and credible alternative explanations.','fbi-behavior,wavr-owner')

for filename,value in [('sources',sources),('terms',terms),('indicators',indicators)]:
    p=ROOT/'data'/f'{filename}.json'
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print(f'{len(terms)} term records, {len(indicators)} observation prompts, {len(sources)} sources')
