import logging
import os
import uuid
import shutil
from urllib.parse import urlparse

from installed_clients.WorkspaceClient import Workspace as workspaceService


class PDBReportUtil:

    def _config_viewer(self, div_id):
        """
            _config_viewer: write the mol* viewer configurations
        """
        return (f'<script type="text/javascript">'
                f'molstar.Viewer.create("{div_id}", {{'
                f'layoutIsExpanded: false,'
                f'layoutShowControls: true,'
                f'layoutShowRemoteState: false,'
                f'layoutShowSequence: true,'
                f'layoutShowLog: true,'
                f'layoutShowLeftPanel: true,'
                f'viewportShowExpand: true,'
                f'viewportShowSelectionMode: true,'
                f'viewportShowAnimation: true,'
                f'collapseLeftPanel: true,'
                f'}}).then(viewer => {{')

    def _save_structure_file(self, dest_dir, pdb):
        """
            _save_structure_file: Place a copy of the structure file to the dest_dir
        """
        file_path = pdb['file_path']
        pdb_file_path = pdb['scratch_path']  # this is the scratch path for this pdb file
        new_pdb_path = os.path.join(dest_dir, os.path.basename(file_path))
        if not pdb.get('from_rcsb', False):
            shutil.copy(pdb_file_path, new_pdb_path)

    def _write_viewer_content_single(self, output_dir, pdb_infos):
        """
            _write_viewer_content_single: write the mol* viewer html content to fill in the
                                        subtabcontent and replace the string
                                        <!--replace subtab content single-->
                                        in the templatefile 'pdb_report_template.html'
        """
        viewer_content = ''
        pdb_index = 0

        for pdb in pdb_infos:
            if pdb.get('from_rcsb', False):
                continue
            file_path = pdb['file_path']
            file_ext = pdb['file_extension'].replace('.', '')
            if file_ext == 'cif':
                file_ext = 'mmcif'
            base_filename = os.path.basename(file_path)

            struct_nm = pdb['structure_name'].upper()
            div_id = 'struct' + str(pdb_index + 1)

            sub_div = (f'<div id="{struct_nm}" class="subtabcontent">'
                       f'<h2>{struct_nm}</h2>'
                       f'<div id="{div_id}" class="app"></div>')

            script_content = self._config_viewer(div_id)
            script_content += (f'viewer.loadStructureFromUrl("./{base_filename}", '
                               f'"{file_ext}", false, {{ representationParams: '
                               f'{{ theme: {{ globalName: "operator-name" }} }} }});'
                               '});')
            script_content += '</script>'

            sub_div += script_content
            sub_div += '</div>'
            viewer_content += sub_div
            pdb_index += 1

        return viewer_content

    def _write_viewer_content_multi(self, output_dir, pdb_infos):
        """
            _write_viewer_content_multi: write the mol* viewer html content to fill in the
                                         subtabcontent and replace the string
                                         <!--replace StructureViewer subtabs-->
                                         in the templatefile 'pdb_report_template.html'
        """
        div_id = 'app_all'
        viewer_script = self._config_viewer(div_id)

        default_click = ''
        viewer_tabs = '<div class="tab">'
        pre_loads = ''

        for pdb in pdb_infos:
            if pdb.get('from_rcsb', False):
                continue
            struct_nm = pdb['structure_name'].upper()
            if not default_click:
                default_click = f'{struct_nm}_sub'
            file_path = pdb['file_path']
            file_ext = pdb['file_extension'].replace('.', '')
            if file_ext == 'cif':
                file_ext = 'mmcif'

            viewer_tabs += (f'<button id="{struct_nm}_sub" '
                            f'class="subtablinks" onclick="openSubTab(event, this)">'
                            f'{struct_nm}</button>')

            pre_loads += (f'viewer.loadStructureFromUrl("./{os.path.basename(file_path)}", '
                          f'"{file_ext}", false, {{ representationParams: '
                          f'{{ theme: {{ globalName: "operator-name" }} }} }});'
                          '});')
        viewer_tabs += '</div>'

        # insert the structure file for preloading
        if pre_loads:
            viewer_script += pre_loads
            viewer_script += '</script>'
            viewer_script += '</div>'
        else:
            viewer_script = ''

        return viewer_tabs, viewer_script, default_click

    def _write_structure_info(self, output_dir, pdb_infos):
        """
            _write_structure_info: write the batch uploaded structure info to replace the string
                                   '<!--replace uploaded pdbs tbody-->' in the tboday tag of the
                                   jQuery DataTable in the template file 'pdb_report_template.html'
        """

        tbody_html = ''
        srv_domain = urlparse(self.shock_url).netloc  # parse url to get the domain portion
        srv_base_url = f'https://{srv_domain}'
        if srv_base_url == 'https://kbase.us':
            srv_base_url = 'https://narrative.kbase.us'

        logging.info(f"Get the url for building the anchor's href: {srv_base_url}")

        for pdb in pdb_infos:
            self._save_structure_file(output_dir, pdb)

            if pdb.get('structure_name', None):
                struct_id = pdb['structure_name'].upper()
            elif pdb.get('rcsb_id', None):
                struct_id = pdb['rcsb_id'].upper()
            else:
                struct_id = 'Unknown strtucture name'

            genome_name = pdb['genome_name']
            genome_ref = pdb['genome_ref']
            feat_id = pdb['feature_id']

            pdb_chains = []
            seq_idens = []
            if pdb.get('chain_ids', None):
                pdb_chains = pdb['chain_ids']
            if pdb.get('sequence_identities', None):
                seq_idens = pdb['sequence_identities']

            # Start writing the tbody content of the table
            tbody_html += '<tr>'
            frm_rcsb = pdb.get('from_rcsb', False)
            if not frm_rcsb:
                tbody_html += (f'<td><div class="subtablinks" '
                               f'onclick="openSubTab(event, this, false)" '
                               f'style="cursor:pointer;color:blue;text-decoration:underline;" '
                               f'title="Click to see in mol*">{struct_id}</div></td>')
            else:
                tbody_html += (f'<td><a href="https://www.rcsb.org/structure/{struct_id}"'
                               f'style="cursor: pointer;" target="_blank" '
                               f'title="3D Structure Viewer">{struct_id}</a></td>')

            tbody_html += (f'<td><a href="{srv_base_url}/#dataview/{genome_ref}"'
                           f' target="_blank">{genome_name}</a></td><td>{feat_id}</td>')
            tbody_html += f'<td>{pdb_chains} </td>'
            tbody_html += f'<td>{seq_idens}</td>'
            tbody_html += '</tr>'

        return tbody_html

    def _retrieve_object(self, obj_ref):
        logging.info('Start retrieving object {}'.format(obj_ref))
        obj_source = self.wsClient.get_objects2(
            {"objects": [{'ref': obj_ref}]})['data'][0]

        obj_info = obj_source.get('info')
        obj_data = obj_source.get('data')

        return obj_info, obj_data

    def __init__(self, config, context):
        self.ws_url = config["workspace-url"]
        self.wsClient = workspaceService(self.ws_url, token=context['token'])
        self.scratch = config['scratch']
        self.shock_url = config['shock-url']
        self.download_dir = None
        self.__baseDownloadUrl = 'https://files.rcsb.org/download'

    def get_pdb_infos(self, params):
        """
            get_pdb_infos: call dfu.get_objects to return pdb_infos

            From input params['protein_structures_ref'] fetch pdb_infos, which is expected to be
            a list of of the following structure,
            e.g.,
            pdb_infos = [{
                'structure_name': '6TUK',
                'file_extension': '.pdb',
                'narrative_id': 63679,
                'genome_name': 'MLuteus_ATCC_49442',
                'feature_id': 'MLuteus_masurca_RAST.CDS.133',
                'is_model': 1,
                'from_rcsb': 1,
                'file_path': os.path.join('/kb/module/test/data', '6TUK.pdb.gz'),
                'genome_ref': '63679/38/1',
                'feature_type': 'gene',
                'sequence_identities': '68.93%',
                'chain_ids': 'Model 1.Chain B',
                'model_ids': '0',
                'exact_matches': '0',
                'scratch_path': os.path.join('/kb/module/test/data', '6TUK.pdb.gz')
            }]
        """
        if 'protein_structures_ref' not in params:
            raise ValueError('Variable "protein_structures_ref" is required!')

        obji, objd = self._retrieve_object(params["protein_structures_ref"])
        return objd.get('pdb_infos', [])

    def generate_html_report(self, params):
        """
            generate_html_report: generates the HTML for the report by calling
            _write_structure_info, _write_viewer_content_single, _write_viewer_content_single
            & _write_viewer_content_multi to generate a report in html and a few DOM sections
            return: the html report and the pdb_infos
        """
        if 'protein_structures_ref' not in params:
            raise ValueError('Variable "protein_structures_ref" is required!')

        pdb_infos = self.get_pdb_infos(params)

        if not pdb_infos:
            return {}

        # Make report directory for writing and copying over uploaded pdb files
        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        os.mkdir(output_directory)

        tbody_html = self._write_structure_info(output_directory, pdb_infos)

        dir_name = os.path.dirname(__file__)
        report_template_file = os.path.join(dir_name, 'templates', 'pdb_report_template.html')
        single_viewer = self._write_viewer_content_single(output_directory, pdb_infos)
        viewer_tabs, multi_viewer, default_click = self._write_viewer_content_multi(
                                                                      output_directory,
                                                                      pdb_infos)
        # Note: multi_viewer is not used because we decide to leave out to speed up the report
        # loading. In case we want to add that tab, would only need to add inside the following
        # `with` block a line of code of:
        #   html_report = html_report.replace('<!--replace subtab content multi-->', multi_viewer)
        # In the meantime, the viewer_tabs should be concatenated with another line like:
        # viewer_tabs += ('<button id="AllStructures_sub" class="subtablinks" '
        #                 'onclick="openSubTab(event, this)">ALL STRUCTURES</button>')
        with open(report_template_file, 'r') as report_template_pt:
            # Fetch & fill in detailed info into template HTML
            if tbody_html:
                html_report = report_template_pt.read()\
                    .replace('<!--replace uploaded pdbs tbody-->', tbody_html)
            if viewer_tabs:
                html_report = html_report\
                    .replace('<!--replace StructureViewer subtabs-->', viewer_tabs)
            if single_viewer:
                html_report = html_report\
                    .replace('<!--replace subtab content single-->', single_viewer)
            html_report = html_report\
                .replace('document.getElementById("AllStructures_sub").click()',
                         f'document.getElementById("{default_click}").click()')
            html_report = html_report.replace('\\', '')
            html_report = html_report.replace('\n', '')

            """
            doms = {
                'table_content': tbody_html,
                'viewer_tabs': viewer_tabs,
                'single_structures': single_viewer,
                'all_structures': multi_viewer
            }
            """

        return {'report_html': html_report}
