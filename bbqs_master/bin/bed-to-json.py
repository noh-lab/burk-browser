"""
This file puts a bed file in the format

gene    start   end     type      prediction

into the json format expected by jbrowse for display
of genomic islands.
"""
import argparse
import json

def read_bed(filepath):
    bed_records = {}
    ids = []
    curr = 0
    with open(filepath) as bed:
        for line in bed:
            line = line.split("\t")
            if line[3] in ids:
                continue
            if line[7] in bed_records.keys():
                bed_records[line[7]].append(build_formatted_record(line, curr))
            else:
                bed_records[line[8]] = [build_formatted_record(line, curr)]
            #bed_records.append(build_record(line, curr))
            ids.append(line[4])
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
        record[2] = -1
    if record[2] == "+":
        record[2] = 1
           
    record[0] = int(record[0])
    record[1] = int(record[1])

    record.insert(0, 0)
    record[-1].strip("\n")

    return record


def to_json_format(bed_data, chunk_name):
    returning = {}
    lazy_loader = {}
    for replicon in bed_data.keys():
        returning[replicon] = {}
        lazy_loader[replicon] = bed_data[replicon]
        nc_list = [[1, bed_data[replicon][0][1], bed_data[replicon][-1][2], 0]]
        returning[replicon]["featureCount"] = len(bed_data[replicon])
        returning[replicon]["formatVersion"] = 1
        returning[replicon]["intervals"] = {}
        returning[replicon]["intervals"]["classes"] = [ 
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
        returning[replicon]["intervals"]["count"] = len(bed_data[replicon])
        returning[replicon]["intervals"]["maxEnd"] = bed_data[replicon][-1][2]
        returning[replicon]["intervals"]["minStart"] = bed_data[replicon][0][1]
        returning[replicon]["intervals"]["lazyClass"] = 1
        returning[replicon]["intervals"]["nclist"] = nc_list
        returning[replicon]["intervals"]["urlTemplate"] = chunk_name + "-{Chunk}.json"

    return lazy_loader, returning
    

def write_json(track_data, out_name, chunk_name, strain):
    for replicon in track_data[1].keys():
        json.dump(track_data[1][replicon], open(f"data/tracks/{strain}/{replicon}/{out_name}", 'w'))
        json.dump(track_data[0][replicon], open(f"data/tracks/{strain}/{replicon}/{chunk_name}-0.json", 'w'))


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
    parser.add_argument('--strain', "-s", type=str, required=False, default="BBQS859",
                        help='the strain on which we are operating (default: %(default)s)')

    args = vars(parser.parse_args())
    write_json(to_json_format(read_bed(args["in"]), args["chunk"]), args["out"], args["chunk"], args["strain"])
    #write_bed(args["in"], read_bed(args["in"]))