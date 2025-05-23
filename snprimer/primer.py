import logging
from dataclasses import dataclass
from dataclasses import field

import gget

from snprimer.position_range import PositionRange


@dataclass
class Primer:
    seq: str
    ref_version: str = "hg19"
    position_ranges: list[PositionRange] = field(default_factory=list, init=True)

    def __post_init__(self):
        if len(self.seq) <= 15:  #povodne 20
            logging.warning(f"Primer {self} is too small to apply the blast and therefore to get information")
        else:
            self._make_blast(self.ref_version)


    def _make_blast(self, ref_version: str):
        blast = gget.blat(self.seq, seqtype="DNA", assembly=ref_version, json=True)
        if blast:
            for hit in gget.blat(self.seq, seqtype="DNA", assembly=ref_version, json=True):
                self.position_ranges.append(
                    PositionRange(hit["chromosome"], hit["start"], hit["end"], hit["strand"], init_snp=False)
                )

    def infos(self, max_vaf=0.1):  # TODO Remove (dont forget README)
        is_ok = True
        if len(self.position_ranges) > 1:
            is_ok = False
            print(f"{self.seq} has multiple potential hybridation sites in the genome.")
        for position_range in self.position_ranges:
            true_snp = position_range.get_snp(max_vaf)
            if true_snp:
                print(f"{self.seq} has snp with vaf > {max_vaf} : {true_snp} ")
                is_ok = False
        if is_ok:
            print(f"{self.seq} is ok")

    def load_all_snps(self):
    #"""Load SNPs for all hybridization places"""
        for position in self.position_ranges:
            position.search_snp()
        return self.position_ranges


if __name__ == "__main__":
    a = Primer("CACACAGATCAGAGGGCCAAC")
    a.infos(0)
