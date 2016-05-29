import json
from segpy import reader
def main():
	output_path = "data.json"
	fh = open("line12.sgy", 'rb')
	segy_reader = reader.create_reader(fh)
	traces = []

	for trace_index in segy_reader.trace_indexes():
		trace = [float(a) for a in segy_reader.trace_samples(trace_index)]
		traces.append(trace)

	traces = traces[:int(len(traces) / 2)]

	json.dump(traces, open(output_path, 'w'))

if __name__ == "__main__":
	main()

