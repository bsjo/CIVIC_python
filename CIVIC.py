#!/usr/bin/env python

import requests, os, datetime


class CIVIC_parsing():
	def __init__(self):
		print("START\n")
		temp_today = datetime.datetime.today()
		self.today = str(temp_today).split(" ")[0]
		print(temp_today)

	def CIVIC_download(self, url, input_path):
		data = requests.get(url)
		r_data = data.text
		self.r_list = r_data.splitlines()
		#CIVIC making
		if not os.path.exists(input_path): os.makedirs(input_path)
		CIVIC_down = '{0}/CIVIC_ClinicalEvidenceSummaries_{1}'.format(input_path, self.today)
		with open(CIVIC_down, 'w') as w:
			w.write(r_data.encode('utf-8'))


	def CIVIC_processing(self, output_path):
		if not os.path.exists(output_path): os.makedirs(output_path)
		output_path_n = os.path.join(output_path, "Parsed_CIVIC_{0}".format(self.today))
		with open(output_path_n, "w") as w:
			header = '\t'.join(['Chromosome', 'Position', 'G_change', 'P_change', 'Gene', "Transcript", 'Origin', 'Disease', 'Drug', 'Evidence', 'Rating']) + '\n'
			w.write(header)
			a = 1
			for line in self.r_list[1:]:
				line = line.encode('utf-8')
				line_split = line.split('\t')
				chrom1 = line_split[21] ; chrom2 = line_split[27]
				G1_pos_start = line_split[22] ; G1_pos_end = line_split[23]
				G2_pos_start = line_split[28] ; G2_pos_end = line_split[29]
				G_pos = '' ; chrom = ''
				if chrom1 :
					if G1_pos_start == G1_pos_end:
						G_pos = G1_pos_start
					else:
						G_pos = G1_pos_start + '-' + G1_pos_end
					chrom = 'chr' + chrom1
					if chrom2 :
						G_pos = G_pos + "," + G2_pos_start + '-' + G2_pos_end
						chrom = chrom + "," + 'chr' + chrom2
				else:
					chrom = ''

				G_change_ref = line_split[24] ; G_change_alt = line_split[25]
				G_change = ''
				if G_change_alt:
					G_change = G_change_ref + ">" + G_change_alt

				P_change = line_split[2] ; Gene = line_split[0] ; origin = line_split[34] ; Transcirpt = line_split[26].split(".")[0]
				Drug = line_split[6] ; rating = line_split[16] ; evidence = line_split[10]
				Disease = line_split[3]
				out_result = '\t'.join([chrom, G_pos, G_change, P_change, Gene, Transcirpt, origin, Disease, Drug, evidence, rating]) + '\n'
				w.write(out_result)

if __name__ == '__main__':

	url = "https://civicdb.org/downloads/nightly/nightly-ClinicalEvidenceSummaries.tsv"
	input_path = 'Input'
	output_path = 'Output'

	#CIVIC_Class
	go = CIVIC_parsing()
	#CIVIC_EvidenceSummary_Download_lastest
	go.CIVIC_download(url, input_path)
	#CIVIC_Parsing
	go.CIVIC_processing(output_path)

	print("\nEND")