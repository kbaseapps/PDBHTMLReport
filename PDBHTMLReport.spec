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


    /* Input/Output of run_PDBHTMLReport
        structure_name: name of the protein structure
        rcsb_id: The structure id for RCSB database
        file_extension: the file extension of the structure, default to 'pdb'
        from_rcsb: indicator if the strcture is from the RCSB Database, default to 0
        is_model: indicator if the strcture is from computational modeling, default to 1
        narrative_id: id of a KBase narrative
        genome_name: name of a KBase genome object
        genome_ref: name of a KBase genome object reference
        feature_id: id of a KBase feature object
        feature_type: id of a KBase feature object's type, default to 'gene'
        file_path: path to the pdb_file file of the pdb structure
        stratch_path: path on the shared folder where the structure file resides, default to file_path
        sequence_identities: sequence identities matched
        chain_ids: protein chain ids
        model_ids: model ids
        exact_matches: a string comma seperated '0' and '1' indicating an exact match not
        found ('0') or found ('1') for the structure's proteins with a given KBase genome feature

        @optional
    */
    typedef structure {
        string structure_name;
        string rcsb_id;
        string file_extension;
        string narrative_id;
        string genome_name;
        string genome_ref;
        string feature_id;
        string feature_type;
        string file_path;
        string scratch_path;
        string sequence_identities;
        string chain_ids;
        string model_ids;
        string exact_matches;
        boolean is_model;
        boolean from_rcsb;
    } PDBHInfo;

    typedef structure {
        list<PDBHInfo> pdb_infos;
    } PDBHTMLReportInput;

    /*
        report_html: a complete html document that can be opened by any browser
        doms: an UnspecifiedObject with DOM html segments that can be used by other apps
    */
    typedef structure {
        string report_html;
        UnspecifiedObject doms;
    } PDBHTMLReportOutput;

    /*
        This function accepts PDBHTMLInput as input parameters and returns an output in a PDBHTMLReport
    */
    funcdef run_PDBHTMLReport(PDBHTMLReportInput params) returns (PDBHTMLReportOutput output) authentication required;

};
