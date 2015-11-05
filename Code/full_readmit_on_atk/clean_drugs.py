__author__ = 'hadoop'

import re
import ast
import string
pattern = re.compile('[^a-zA-Z]+')
stopwords = ['mg', 'ml', 'units', 'gram', 'mcg']

# in: list of unclean words as a "string representation of a list of strings",
# like a JSon representation of a list of strings

# out: 'document', a single string of the cleaned words separated by '|'

def to_clean_doc(text, delimiter='|'):
    text = re.sub(pattern, ' ', text)
    text = text.lower()
    tokens = text.split()
    tokens = [w for w in tokens if w not in stopwords]
    tokens = [w for w in tokens if len(w)>2]
    tokens = map(preprocess, tokens)
    tokens = [w for w in tokens if len(w)>0]
    return delimiter.join(tokens)




re_capsule = re.compile(r'capsules?')
re_oraltablet = re.compile(r'oral\stablets?')
re_oraltablet = re.compile(r'oral\stabs?')
re_oralliquid = re.compile(r'oral\sliquid?')
re_oralliquid = re.compile(r'oral\sdose?')
re_oralsuspension = re.compile(r'oral\ssuspensions?')
re_suspension = re.compile(r'suspensions?')
re_tablet = re.compile(r'tablets?')
re_intrathecal = re.compile(r'intrathecall?y?')

STOPS = [re_capsule, re_oraltablet, re_oralliquid, re_oralsuspension, re_suspension, re_tablet, re_intrathecal]
def preprocess(med):
	med = med.lower()
	for stop in STOPS:
		med = re.sub(stop, '', med)
	if len(re.findall(r'^(admission\slabs?|abdomen|abdominal)', med)) != 0:
		med = ''
	if len(re.findall(r'^(accucheck|accuchek|accu\schek|accu\scheck)', med)) != 0:
		med = 'accucheck'
	if len(re.findall(r'^glucose\stest\sstrips?', med)) != 0:
		med = 'glucose test strips'
	if len(re.findall(r'^insulin\ssliding\sscale', med)) != 0:
		med = 'insulin sliding scale'
	if len(re.findall(r'^insulin\ssyringes', med)) != 0:
		med = 'insulin syringes'
	if len(re.findall(r'^insulin.*?daily', med)) != 0:
		med = 'insulin daily'
	if len(re.findall(r'^lantus', med)) != 0:
		med = 'lantus'
	if len(re.findall(r'^acetaminophen\scodeine', med)) != 0:
		med = 'acetaminophen codeine'
	elif len(re.findall(r'^acetaminophen', med)) != 0:
		med = 'acetaminophen'
	if len(re.findall(r'advair', med)) != 0:
		med = 'advair'
	if len(re.findall(r'advil', med)) != 0:
		med = 'advil'
	if len(re.findall(r'^afrin', med)) != 0:
		med = 'afrin'
	if len(re.findall(r'^albuterol', med)) != 0:
		med = 'albuterol'
	if len(re.findall(r'^zofran', med)) != 0:
		med = 'zofran '
	if len(re.findall(r'^zinc\soxide', med)) != 0:
		med = 'zinc oxide'
	if len(re.findall(r'^zinc\ssulfate', med)) != 0:
		med = 'zinc sulfate'
	if len(re.findall(r'^zinc\ssupplement', med)) != 0:
		med = 'zinc supplement'
	if len(re.findall(r'^zantac', med)) != 0:
		med = 'zantac'
	if len(re.findall(r'^xenaderm', med)) != 0:
		med = 'xenaderm'
	if len(re.findall(r'^wound\scare', med)) != 0:
		med = 'wound care'
	if len(re.findall(r'^chloraseptic', med)) != 0:
		med = 'chloraseptic'
	if len(re.findall(r'^cholecalciferol', med)) != 0:
		med = 'cholecalciferol'
	if len(re.findall(r'^amphotericin', med)) != 0:
		med = 'amphotericin'
	if len(re.findall(r'^artificial\stears?', med)) != 0:
		med = 'artificial tears'
	if len(re.findall(r'^warfarin', med)) != 0:
		med = 'warfarin'
	if len(re.findall(r'^prednisone', med)) != 0:
		med = 'prednisone'
	if len(re.findall(r'^percocet', med)) != 0:
		med = 'percocet'
	if len(re.findall(r'^benadryl', med)) != 0:
		med = 'benadryl'
	if len(re.findall(r'^vancomycin', med)) != 0:
		med = 'vancomycin'
	if len(re.findall(r'^vanco', med)) != 0:
		med = 'vanco'
	if len(re.findall(r'^bisacodyl', med)) != 0:
		med = 'bisacodyl'
	if len(re.findall(r'^nitroglycerin', med)) != 0:
		med = 'nitroglycerin'
	if len(re.findall(r'^acyclovir\soral', med)) != 0:
		med = 'acyclovir'
	if len(re.findall(r'(acylovir|acycl)$', med)) != 0:
		med = 'acylovir'
	if len(re.findall(r'^alpraz', med)) != 0:
		med = 'alprazolam'
	if len(re.findall(r'^(alprazolam)', med)) != 0:
		med = 'alprazolam'
	if len(re.findall(r'^ambien', med)) != 0:
		med = 'ambien'
	if len(re.findall(r'^carnation', med)) != 0:
		med = 'carnation instant breakfast'
	if len(re.findall(r'^cepacol', med)) != 0:
		med = 'cepacol'
	if len(re.findall(r'^coumadin', med)) != 0:
		med = 'coumadin'
	if len(re.findall(r'^ensure', med)) != 0:
		med = 'ensure'
	if len(re.findall(r'^fluticasone', med)) != 0:
		med = 'fluticasone'
	if len(re.findall(r'^hydrocortisone', med)) != 0:
		med = 'hydrocortisone'
	if len(re.findall(r'^(insulin|novolog)', med)) != 0:
		med = 'insulin'
	if len(re.findall(r'^multivitamin', med)) != 0:
		med = 'multivitamin'
	if len(re.findall(r'^normal\ssaline', med)) != 0:
		med = 'normal saline'
	if len(re.findall(r'^oxygen', med)) != 0:
		med = 'oxygen'
	if len(re.findall(r'^calcium\sacetate', med)) != 0:
		med = 'calcium acetate'
	if len(re.findall(r'^calcium\scarbonate', med)) != 0:
		med = 'calcium carbonate'
	if len(re.findall(r'^calcium\schloride', med)) != 0:
		med = 'calcium chloride'
	if len(re.findall(r'^calcium\smagnesium', med)) != 0:
		med = 'calcium magnesium'
	if len(re.findall(r'^aspirin', med)) != 0:
		med = 'aspirin'
	if len(re.findall(r'^sodium\schloride', med)) != 0:
		med = 'sodium chloride'
	if len(re.findall(r'^ferrous\ssulfate', med)) != 0:
		med = 'ferrous sulfate'
	if len(re.findall(r'^motel', med)) != 0:
		med = 'motelukast'
	#
	if len(re.findall(r'^(picc|comprehensive\smetabolic\spanel|blood|with|work|wound|whom|wheelchair|(rolling\s)?walker|water|cervical|check|chem|chest|commode|complete|continue|continuous|contour|contrast|dexamethasone|diabetes|diabetic|diagnosis|dressing|emergency|emergencies|gauze|have|head|home|hospice|hospital|interventional|investigational|laboratory|labs?\s|labwork|lateral|needle|panel|patient|physical\stherapy|please|portable|questions?|saline|script|scan|sliding|sling|speech|supplemental\soxygen|this|total|touch|tube|twice\sweekly|upright|will\sneed|with\sdiff|would\sscare|chest\sxray|draw|outpatient|basic\smetabolic\spanel|visiting\snurse|needs?\s|stat\slabs?|should\shave|brain|alcohol|alchol)', med)) != 0:
		med = ''
	med = re.sub(r'^(daily|week?ly|monthly|days?)', '', med)
	med = re.sub(r'(daily|week?ly|monthly|days?)$', '', med)
	tmpmed = med
	med = re.sub(r'(home\sdose|ivbp|ivpb|let(\s(once|twice))?|liquid|disp)$', '', med)
	med = re.sub(r'(caps|hours|solution|(piggyback\s)?every.*?|every\shours|powder\sinjection|intravenous\s?(injection|solution)?|oral|tabs|topical\s?(cream|topical\scream|ointment)|(let)?\sstop\sdate)$', '', med)
	med = re.sub(r'(extended\srelease|extended\srelease\slet\sextended\srelease|let|oral|oral\sconcentrate|orally\sdisintegrating\s(once|twice)\shome|)$', '', med)
	med = re.sub(r'(compounding\spowder|home\smedication|intrathecal|le|let|let\sthree\stimes|oral|oral\sliquid|orally(\smorning|evening)(\sorally\s(morning|evening))?)$', '', med)

	med = re.sub(r'\s+', ' ', med)
	med = med.strip()

	# if len(med.split()) > 4:
	return med