"""
This file puts a bed file in the format

gene    start   end     type      prediction

into the json format expected by jbrowse for display
of genomic islands.
"""
import argparse
import json

def read_bed(filepath):
    bed_records = []
    curr = 0
    with open(filepath) as bed:
        for line in bed:
            line = line.split("\t")
            bed_records.append(build_record(line, curr))
            curr += 1

    return bed_records


def build_record(record, id):
    returning = []
    returning.append(0)
    returning.append(record[1]) # start
    returning.append(record[2]) # end
    returning.append(1) # strand
    returning.append(record[3]) # name
    returning.append(record[4].strip("\n")) # note
    returning.append(0) # phase
    returning.append(record[0]) # replicon
    returning.append("chromosome_"+record[0][-3]) # seq_id
    returning.append(record[4].strip("\n").split(" ")[2]) # source
    returning.append("genomic island") # type

    return returning


def to_json_format(bed_data):
    returning = {}
    returning["featureCount"] = len(bed_data)
    returning["formatVersion"] = 1
    returning["intervals"] = {}
    returning["intervals"]["classes"] = [ 
                                            { "attributes": 
                                                [
                                                    "Start",
                                                    "End",
                                                    "Strand",
                                                    "Id",
                                                    "Name",
                                                    "Note",
                                                    "Phase",
                                                    "Replicon",
                                                    "Seq_id",
                                                    "Source",
                                                    "Type"
                                                ],
                                                "isArrayAttr": {}
                                            },
                                            { "attributes": [
                                                    "Start",
                                                    "End",
                                                    "Chunk"
                                                ],
                                                "isArrayAttr": {
                                                    "Sublist": 1
                                                }
                                            }
                                        ]
    returning["intervals"]["count"] = len(bed_data)
    returning["intervals"]["lazyClass"] = 1
    returning["intervals"]["maxEnd"] = bed_data[-1][3]
    returning["intervals"]["minStart"] = bed_data[0][1]
    returning["intervals"]["nclist"] = bed_data
    returning["intervals"]["urlTemplate"] = "lf-{Chunk}.json"

    return returning
    


def write_json(formatted, out_name):
    json.dump(formatted, open(out_name, 'w'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a BED file into JSON format.')
    parser.add_argument('--in', "-i", type=str, required=False, default="islandData.bed",
                        help='the name of the BED file to be processed (default: %(default)s)')
    parser.add_argument('--out', "-o", type=str, required=False, default="trackData.json",
                        help='the name of the JSON file to write (default: %(default)s)')

    args = vars(parser.parse_args())
    write_json(to_json_format(read_bed(args["in"])), args["out"])