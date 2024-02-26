import csv
import sys
from ruamel.yaml import YAML, scalarstring

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

def csv_to_yaml(csv_file, yaml_file, desired_order):
  """Converts a CSV file to a YAML file, handling multiple resource records."""

  data = {}
  with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='\'')
    # Type,Name,Value
    # CNAME,nn7dfx2vndu4c2zycwq2a65haxt2tnfv._domainkey.lionsfestivals.com,nn7dfx2vndu4c2zycwq2a65haxt2tnfv.dkim.amazonses.com
    for row in reader:
      name = row['Name'] + '.'
      type = row['Type']
      ttl = 86400
      key = (row['Name'], row['Type'])  # Combine Name and Type as key
      resource_records = row['Value'].split('|')
      new_resource_records = []
      for resource_record in resource_records:
        if "\"" in resource_record:
          new_resource_record = scalarstring.SingleQuotedScalarString(resource_record + '.')
        else:
          new_resource_record = scalarstring.DoubleQuotedScalarString(resource_record + '.')
        new_resource_records.append(new_resource_record)
      resource_records = new_resource_records
      

      data.setdefault(key, {}).update({
       'Name': scalarstring.DoubleQuotedScalarString(name),
       'Type': scalarstring.DoubleQuotedScalarString(type),
       'TTL': scalarstring.DoubleQuotedScalarString(ttl),
       'ResourceRecords': resource_records
      })

  with open(yaml_file, 'w') as yamlfile:
    #yaml.dump(list(data.values()), yamlfile, default_flow_style=False, sort_keys=False)
    yaml.dump(list(data.values()), yamlfile)

if __name__ == '__main__':
  csv_file = 'dkim-dns-records.csv'
  csv_file = sys.argv[1]
  yaml_file = 'output.yaml'
  desired_order = ["Name", "Type", "TTL", "ResourceRecords"]
  csv_to_yaml(csv_file, yaml_file, desired_order)
