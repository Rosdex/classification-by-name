# -*- encoding: utf-8 -*-
import os
import subprocess
import xml.etree.ElementTree as ElementTree
import sys
import csv
    
def show_facts(facts):
    for fact in facts:
        print("{0} {1} - len is {2}".format(fact['fact'], fact['adjForName'], fact['len']))
        
def facts_to_string(facts):
    result_str = ''
    
    for fact in facts:
        result_str += "{0} {1} ".format(fact['fact'], fact['adjForName'])
    
    result_str = result_str.lower().strip()
    
    return result_str
    
def fact_to_string(fact):
    result_str = "{0} {1} ".format(fact['fact'], fact['adjForName'])
    result_str = result_str.lower().strip()
    return result_str
    
    

class TomitaParser(object):
    def __init__(self, executable, config, debug=True, validate=True):
        self.debug_mode = debug
        self.debug("Init Tomita Parser...")

        self.executable = os.path.expanduser(executable)
        if not os.path.exists(self.executable):
            raise Exception("Tomita executable not found at: %s" % self.executable)

        self.debug("Executable: %s" % self.executable)

        self.config = os.path.expanduser(config)
        if not os.path.exists(self.config):
            raise Exception("Config file not found at: %s" % self.config)

        self.debug("Config: %s" % self.config)

        self.path = self.config[:self.config.rfind('\\')]

        self.debug("Path: %s" % self.path)
        self.debug("ZBS!")

        if validate:
            self.validate_config()

    def validate_config(self):
        is_xml = False
        with open(self.config, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    if line.startswith("File"):
                        raise Exception("This library uses STDIN and STDOT for communicating with Tomita Parser, "
                                        "please remove all File = \"...\" from Input and Output sections in config.")
                    if line.startswith("Format") and "xml" in line:
                        is_xml = True
        if not is_xml:
            raise Exception("This library working only with XML output, "
                            "please add \"Format = xml;\" to the Output section.")

    def run(self, text, with_facts=True, with_leads=True):
        self.debug("Running Tomita Parser...")
        
        pipe = subprocess.Popen(
            [self.executable, self.config],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.path
        )
        out, err = pipe.communicate(input=text.encode("utf-8"))

        self.debug(err)
        
        facts = []
        leads = []
        etree_root = ElementTree.fromstring(out)
        if etree_root.find("document") is not None:
            if with_facts:
                self.debug("Parsing facts...")
                for fact in etree_root.find("document").find("facts"):
                    # adj for name is optional field. So we need check that they are exist
                    adjForName = fact.find("AdjForName")
                    adjForName = adjForName.attrib.get("val") if adjForName is not None else ''
                
                    facts.append({
                        "fact_id": fact.attrib.get("FactID"),
                        "lead_id": fact.attrib.get("LeadID"),
                        "pos": fact.attrib.get("pos"),
                        "len": fact.attrib.get("len"),
                        "fact": fact.find("Name").attrib.get("val"),
                        "adjForName": adjForName,
                    })

            if with_leads:
                self.debug("Parsing leads...")
                for lead in etree_root.find("document").find("Leads"):
                    leads.append({
                        "lead_id": lead.attrib.get("id"),
                        "lead": lead.attrib.get("text")
                    })

        return facts, leads

    def debug(self, text):
        if self.debug_mode:
            print(text)
            
if __name__ == "__main__":
    filename = sys.argv[1]
    target_categiry = sys.argv[2]

    print('Handle file: {0}'.format(filename))
    
    facts = []
    leads = []
    
    output_strings = []
    
    with open(filename, newline='', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            print('Handle string: {0}'.format(row[0]))
            
            tomita = TomitaParser('C:\\Temp\\Rosdex-ML\\classification_by_name\\ClearNames\\tomitaparser.exe', 'C:\\Temp\\Rosdex-ML\\classification_by_name\\ClearNames\\tomita_config\\config.proto', debug=False)
            facts, leads = tomita.run(row[0])
            
            show_facts(facts)
            
            #sort facts by length
            #sorted_facts = sorted(facts, key=lambda k: k['len'])
            #take fact with max length
            #clear_name = fact_to_string(sorted_facts[0])
            
            #take all facts
            #clear_name = facts_to_string(facts)
            
            #take only first fact
            clear_name = fact_to_string(facts[0])
            
            
            print('Clear name is {0}'.format(clear_name))
            
            output_strings.append('{0},{1}'.format(clear_name,row[1]))
            
    with open('Category_{0}_clear_names.csv'.format(target_categiry),'wt', encoding="utf8") as file:
        for str in output_strings:
            file.write(str)
            file.write('\n')