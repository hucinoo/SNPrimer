import re
from typing import List, Dict, NamedTuple
import os 

snp_list =[]
class SNP(NamedTuple):
    id: str
    rsid: str
    vaf: float

class PositionRange(NamedTuple):
    chr: str
    start: int
    end: int
    strand: str
    snps: List[SNP]

def parse_genomic_data():
    
    with open('./output.txt', 'r') as file:
        data = file.read()
        
    #print(content)
    # Split the input to get the primer sequence
    lines = data.strip().split('\n')
    primer = lines[0]
    
    # Extract all PositionRange blocks
    position_blocks = re.findall(r'PositionRange\(.*?\)(?=\s*,\s*Position|\s*\])', data, re.DOTALL)
    parsed_ranges = []
    for block in position_blocks:
        # Extract chromosome, start, end, and strand
        chr_match = re.search(r"chr='([^']+)'", block)
        start_match = re.search(r"start=(\d+)", block)
        end_match = re.search(r"end=(\d+)", block)
        strand_match = re.search(r"strand='([^']+)'", block)
        
        # Extract all SNPs
        snp_matches = re.findall(r"SNP\(id='([^']+)', rsid='([^']+)', vaf=([^)]+)\)", block)
        
        snps = []
        for id_val, rsid, vaf in snp_matches:
            snps.append(SNP(id=id_val, rsid=rsid, vaf=float(vaf)))
        
        if chr_match and start_match and end_match and strand_match:
            position_range = PositionRange(
                chr=chr_match.group(1),
                start=int(start_match.group(1)),
                end=int(end_match.group(1)),
                strand=strand_match.group(1),
                snps=snps
            )
            parsed_ranges.append(position_range)
        
            
    for i, pos_range in enumerate(parsed_ranges, 1):
        #print(f"Primer: {result['primer']}")
        print(f"\n{i}. Position Range:")
        print(f"   Chromosome: {pos_range.chr}")
        print(f"   Start: {pos_range.start}")
        print(f"   End: {pos_range.end}")
        print(f"   Strand: {pos_range.strand}")
        print(f"   SNPs ({len(pos_range.snps)}):")
        with open("snp_output.txt", "a") as file:
            file.write(f"{i}. Location: {pos_range.chr}:{pos_range.start}-{pos_range.end},Strand: {pos_range.strand}\n")
        
        # Group SNPs by unique ID to remove duplicates
        unique_snps = {}
        for snp in pos_range.snps:
            key = (snp.id, snp.rsid)
            if key not in unique_snps:
                unique_snps[key] = snp
    
        #with open("output.txt", "w") as file:
        #   for j, snp in enumerate(unique_snps.values(), 1):
            # Write the formatted string to the file
        #      file.write(f"      {j}. ID: {snp.id}, RSID: {snp.rsid}, VAF: {snp.vaf}\n")
        #     print(f"      {j}. ID: {snp.id}, RSID: {snp.rsid}, VAF: {snp.vaf}")
        for j, snp in enumerate(unique_snps.values(), 1):
            print(f"    {j}. ID: {snp.id}, RSID: {snp.rsid}, VAF: {snp.vaf}")
            snp_list.append(f"  {j}. ID: {snp.id}, RSID: {snp.rsid}, VAF: {snp.vaf}")
            with open("snp_output.txt", "a") as file:
        #   for j, snp in enumerate(unique_snps.values(), 1):
            # Write the formatted string to the file
                file.write(f"   {j}. ID: {snp.id}, RSID: {snp.rsid}, VAF: {snp.vaf}\n")