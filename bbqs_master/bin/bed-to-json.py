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
    ids = []
    curr = 0
    with open(filepath) as bed:
        for line in bed:
            line = line.split("\t")
            if line[3] in ids:
                continue
            #bed_records.append(build_record(line, curr))
            bed_records.append(build_formatted_record(line, curr))
            ids.append(line[3])
            curr += 1

    return bed_records


def build_record(record, id):
    returning = []
    
    returning.append(0)
    returning.append(int(record[1])-1) # start
    returning.append(int(record[2])) # end
    returning.append(1) # strand
    returning.append("island_"+str(id)) # id
    returning.append(record[3]) # name
    returning.append(record[4].strip("\n")) # note
    returning.append("0") # phase
    returning.append("chromosome_"+record[0][-3]) # seq_id
    returning.append(record[0]) # replicon
    returning.append(record[4].strip("\n").split(" ")[2]) # source
    returning.append("genomic island") # type

    return returning


def build_formatted_record(record, curr):
    if record[2] == "-":
        record[2] = "-1"
    if record[2] == "+":
        record[2] = "1"

    return record


def to_json_format(bed_data, chunk_name):
    returning = {}
    lazy_loader = bed_data
    nc_list = [[1, bed_data[0][1], bed_data[-1][2], 0]]
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
                                            "isArrayAttr": {}
            }
                                        ]
    returning["intervals"]["count"] = len(bed_data)
    returning["intervals"]["maxEnd"] = bed_data[-1][2]
    returning["intervals"]["minStart"] = bed_data[0][1]
    returning["intervals"]["lazyClass"] = 1
    returning["intervals"]["nclist"] = nc_list
    returning["intervals"]["urlTemplate"] = chunk_name + "-{Chunk}.json"

    return lazy_loader, returning
    

def write_json(track_data, out_name, chunk_name, path):
    json.dump(track_data[1], open(out_name, 'w'))
    json.dump(track_data[0], open(path + chunk_name + "-0.json", 'w'))


def write_bed(filename, bed_data):
    with open(filename+".fixed", "w") as f:
        f.write("start\tend\tstrand\tid\tname\tnote\tphase\treplicon\tseq_id\tsource\ttype\n")
        for record in bed_data:
            f.write("\t".join(record)+"\n")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a BED file into JSON format.')
    parser.add_argument('--in', "-i", type=str, required=False, default="islandData.bed",
                        help='the name of the BED file to be processed (default: %(default)s)')
    parser.add_argument('--out', "-o", type=str, required=False, default="trackData.json",
                        help='the name of the JSON file to write (default: %(default)s)')
    parser.add_argument('--chunk', "-c", type=str, required=False, default="bed",
                        help='the name of the chunk files to write to (default: %(default)s)')
    parser.add_argument('--path', "-p", type=str, required=False, default="data/tracks/",
                        help='the path to put chunk files (default: %(default)s)')

    args = vars(parser.parse_args())
    write_json(to_json_format(read_bed(args["in"]), args["chunk"]), args["out"], args["chunk"], args["path"])
    #write_bed(args["in"], read_bed(args["in"]))