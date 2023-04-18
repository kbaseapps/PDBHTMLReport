# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from PDBHTMLReport.Utils.PDBReportUtil import PDBReportUtil
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
    GIT_URL = "https://github.com/qzzhang/PDBHTMLReport.git"
    GIT_COMMIT_HASH = "3f4a4b93d540f1313ecf35bae3c8e8bb05f5f244"

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
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass

    def get_PDBInfos(self, ctx, params):
        """
        This function accepts PDBHTMLInput as input parameters and returns an object pdf_infos
        :param params: instance of type "PDBHTMLInput" -> structure:
           parameter "protein_structures_ref" of type "obj_ref" (An X/Y/Z
           style reference @id ws)
        :returns: instance of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN get_PDBInfos
        self.config['USER_ID'] = ctx['user_id']
        self.pdb_report_util = PDBReportUtil(self.config)

        output = self.pdb_report_util.get_pdb_infos(params)
        #END get_PDBInfos

        # At some point might do deeper type checking...
        if not isinstance(output, object):
            raise ValueError('Method get_PDBInfos return value ' +
                             'output is not type object as required.')
        # return the results
        return [output]

    def run_PDBHTMLReport(self, ctx, params):
        """
        This function accepts PDBHTMLInput as input parameters and returns an output in a PDBHTMLReport
        :param params: instance of type "PDBHTMLInput" -> structure:
           parameter "protein_structures_ref" of type "obj_ref" (An X/Y/Z
           style reference @id ws)
        :returns: instance of type "PDBHTMLReportOutput" (report_html: a
           complete html document that can be opened by any browser doms: an
           UnspecifiedObject with DOM html segments that can be used by other
           apps) -> structure: parameter "report_html" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_PDBHTMLReport
        self.config['USER_ID'] = ctx['user_id']
        self.pdb_report_util = PDBReportUtil(self.config)

        output = self.pdb_report_util.generate_html_report(params)

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
