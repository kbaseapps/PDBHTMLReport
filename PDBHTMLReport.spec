/*
A KBase module: PDBHTMLReport
*/

module PDBHTMLReport {
    /* A boolean - 0 for false, 1 for true.
       @range (0, 1)
    */
    typedef int boolean;

    /* workspace name of the object */
    typedef string workspace_name;

    /* An X/Y/Z style reference
      @id ws
    */
    typedef string obj_ref;

    typedef structure {
        obj_ref protein_structures_ref;
    } PDBHTMLInput;

    /*
        report_html: a complete html document that can be opened by any browser
        doms: an UnspecifiedObject with DOM html segments that can be used by other apps
    */
    typedef structure {
        string report_html;
    } PDBHTMLReportOutput;

    /*
        This function accepts PDBHTMLInput as input parameters and returns an object pdf_infos 
    */
    funcdef get_PDBInfos(PDBHTMLInput params) returns (UnspecifiedObject output) authentication required;

    /*
        This function accepts PDBHTMLInput as input parameters and returns an output in a PDBHTMLReport
    */
    funcdef run_PDBHTMLReport(PDBHTMLInput params) returns (PDBHTMLReportOutput output) authentication required;

};
