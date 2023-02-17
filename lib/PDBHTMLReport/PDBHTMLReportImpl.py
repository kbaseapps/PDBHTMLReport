# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
from PDBHTMLReport.Utils.PDBUtil import PDBUtil
#END_HEADER


class PDBHTMLReport:
    '''
    Module Name:
    PDBHTMLReport

    Module Description:
    A KBase module: PDBHTMLReport
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "HEAD"

    #BEGIN_CLASS_HEADER
    '''
    PDBHTMLReport will take a metadata file from the staging area and output an html report
    '''
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_PDBHTMLReport(self, ctx, params):
        """
        This function accepts PDBHTMLInput as input parameters and returns an output in a PDBHTMLReport
        :param params: instance of type "PDBHTMLReportInput" (Input/Output of
           run_PDBHTMLReport structures_name: Proteinstructures object name
           workspace_name: workspace name for object to be saved to
           metadata_staging_file_path: path to a spreadsheet file that lists
           the metadata of PDB files and their KBase metadata) -> structure:
           parameter "metadata_staging_file_path" of String, parameter
           "structures_name" of String, parameter "workspace_name" of type
           "workspace_name" (workspace name of the object)
        :returns: instance of type "PDBHTMLReportOutput" -> structure:
           parameter "report_dir" of String, parameter "report_name" of
           String, parameter "report_description" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_PDBHTMLReport
        self.config['USER_ID'] = ctx['user_id']
        self.pdb_util = PDBUtil(self.config)
        
        output = self.pdb_util.generate_html_report(params)

        #END run_PDBHTMLReport

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_PDBHTMLReport return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
