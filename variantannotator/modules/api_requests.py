"""
This module creates an object that creates requests to call data from the VariantValidator API
"""
import requests


class VvRest:
    def __init__(self):
        # self.base_url = "http://127.0.0.1:8080/"
        self.base_url = "https://rest.variantvalidator.org"
        self.lovd_call = "{}/LOVD/lovd/{}/{}/{}/{}/{}/{}"

    def lovd(self, genome_build, variant_description, transcript_model="refseq",  select_transcripts="all",
             check_only=False, liftover=True, return_format="json"):
        """
        Method that calls the VariantValidator API  LOVD endpoint. This tool is a rapid g. > c. > p. tool so is ideal
        for validating genomic variant descriptions and accessing c. and p.

        For fastest processing, set liftover to False and specify a transcript, or limited transcripts

        :param genome_build: One of GRCh37, GRCh38, hg19 or hg38
        :param variant_description: Must be a genomic description in the pseudo vcf chr-pos-ref-alt or g. hgvs
        :param transcript_model: refseq or ensembl
        :param select_transcripts: all, select, mane, mane_select, or specific transcript or transcripts delimited by |
        :param check_only: Do not map to any transcripts if true, just validate the genomic description
        :param liftover: Lift to other genome build (e.g. 37 to 38)
        :param return_format: json or xml
        :return: Validation response
        """
        url = self.lovd_call.format(self.base_url,
                                    genome_build,
                                    variant_description,
                                    transcript_model,
                                    select_transcripts,
                                    check_only,
                                    liftover)

        if return_format == 'json':
            url = url + "?content-type=application/json"
        elif return_format == 'xml':
            url = url + "?content-type=application/xml"
            pass

        lovd_response = requests.get(url)
        return lovd_response

