"""
This file puts a bed file in the format

start   end     strand      id      name    details     phase     seq_id    replicon    source      type

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
            line = list(filter(None, line.split("\t")))
            if line[3] in ids:
                continue
            if line[7] in bed_records.keys():
                bed_records[line[7]].append(build_formatted_record(line, curr))
            else:
                bed_records[line[8]] = [build_formatted_record(line, curr)]
            ids.append(line[4])
            curr += 1

    return bed_records


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
    for seq_id in bed_data.keys():
        returning[seq_id] = {}
        lazy_loader[seq_id] = bed_data[seq_id]
        nc_list = [[1, bed_data[seq_id][0][1], bed_data[seq_id][-1][2], 0]]
        returning[seq_id]["featureCount"] = len(bed_data[seq_id])
        returning[seq_id]["formatVersion"] = 1
        returning[seq_id]["intervals"] = {}
        returning[seq_id]["intervals"]["classes"] = [
            {"attributes":
                                                    [
                                                        "Start",
                                                        "End",
                                                        "Strand",
                                                        "Id",
                                                        "Name",
                                                        "Note",
                                                        "Phase",
                                                        "Seq_id",
                                                        "Replicon",
                                                        "Source",
                                                        "Type"
                                                    ],
             "isArrayAttr": {}
             },
            {"attributes": [
                "Start",
                "End",
                "Chunk"
            ],
                "isArrayAttr": {}
            }
        ]
        returning[seq_id]["intervals"]["count"] = len(bed_data[seq_id])
        returning[seq_id]["intervals"]["maxEnd"] = bed_data[seq_id][-1][2]
        returning[seq_id]["intervals"]["minStart"] = bed_data[seq_id][0][1]
        returning[seq_id]["intervals"]["lazyClass"] = 1
        returning[seq_id]["intervals"]["nclist"] = nc_list
        returning[seq_id]["intervals"]["urlTemplate"] = chunk_name + \
            "-{Chunk}.json"

    return lazy_loader, returning


def write_json(track_data, out_name, chunk_name, strain):
    for seq_id in track_data[1].keys():
        json.dump(track_data[1][seq_id], open(
            f"data/tracks/{strain}/{seq_id}/{out_name}", 'w'))
        json.dump(track_data[0][seq_id], open(
            f"data/tracks/{strain}/{seq_id}/{chunk_name}-0.json", 'w'))


def write_bed(filename, bed_data):
    with open(filename+".fixed", "w") as f:
        f.write(
            "start\tend\tstrand\tid\tname\tnote\tphase\tseq_id\treplicon\tsource\ttype\n")
        for record in bed_data:
            f.write("\t".join(record)+"\n")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Process a BED file into JSON format.')
    parser.add_argument('--in', "-i", type=str, required=False, default="islandData.bed",
                        help='the name of the BED file to be processed (default: %(default)s)')
    parser.add_argument('--out', "-o", type=str, required=False, default="trackData.json",
                        help='the name of the JSON file to write (default: %(default)s)')
    parser.add_argument('--chunk', "-c", type=str, required=False, default="bed",
                        help='the name of the chunk files to write to (default: %(default)s)')
    parser.add_argument('--strain', "-s", type=str, required=False, default="BBQS859",
                        help='the strain on which we are operating (default: %(default)s)')

    args = vars(parser.parse_args())
    write_json(to_json_format(read_bed(
        args["in"]), args["chunk"]), args["out"], args["chunk"], args["strain"])
    #write_bed(args["in"], read_bed(args["in"]))
