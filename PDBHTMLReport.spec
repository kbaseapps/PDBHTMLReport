/*
A KBase module: PDBHTMLReport
*/

module PDBHTMLReport {

    /* workspace name of the object */
    typedef string workspace_name;

    /* An X/Y/Z style reference
      @id ws
    */
    typedef string obj_ref;


    /* Input/Output of run_PDBHTMLReport
        structures_name: Proteinstructures object name
        workspace_name: workspace name for object to be saved to
        metadata_staging_file_path: path to a spreadsheet file that lists the metadata of PDB files and their KBase metadata
    */
    typedef structure {
        string metadata_staging_file_path;
        string structures_name;
        workspace_name workspace_name;
    } PDBHTMLReportInput;

    typedef structure {
        string report_dir;
        string report_name;
        string report_description;
    } PDBHTMLReportOutput;

    /*
        This function accepts PDBHTMLInput as input parameters and returns an output in a PDBHTMLReport
    */
    funcdef run_PDBHTMLReport(PDBHTMLReportInput params) returns (PDBHTMLReportOutput output) authentication required;

};
