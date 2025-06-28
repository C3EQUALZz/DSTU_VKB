/*
This file is part of OmniDB.
OmniDB is open-source software, distributed "AS IS" under the MIT license in the hope that it will be useful.

The MIT License (MIT)

Portions Copyright (c) 2015-2020, The OmniDB Team
Portions Copyright (c) 2017-2020, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
import { createRequest } from "../long_polling";
import { queryRequestCodes } from "../constants";
import { checkDebugStatus } from "../debug";

let createDebuggerTabFunction = function(p_function) {
  // Removing last tab of the inner tab list.
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  // Updating inner tab_name.
  var v_name = 'Debugger: ' + p_function;

  let v_name_html =
  '<span id="tab_title">' +
    v_name +
  '</span>' +
  '<span id="tab_loading" style="visibility:hidden;">' +
    '<i class="tab-icon node-spin"></i>' +
  '</span>' +
  '<i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i>';

  // Creating debug tab in the inner tab list.
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_icon: '<i class="fas fa-code-branch icon-tab-title"></i>',
    p_name: v_name_html,
    p_selectFunction: function() {
      if(this.tag != null) {
        this.tag.resize();
      }
      if(this.tag != null && this.tag.editor != null) {
          this.tag.editor.focus();
          checkDebugStatus(this);
      }
    },
    p_closeFunction: function(e,p_tab) {
      var v_current_tab = p_tab;
      beforeCloseTab(e,
        function() {
          var v_message_data = { tab_id: v_current_tab.tag.tab_id, tab_db_id: null };
          createRequest(queryRequestCodes.CloseTab, [v_message_data]);
          v_current_tab.removeTab();
          if (v_tab.tag.tabCloseFunction)
            v_tab.tag.tabCloseFunction(v_tab.tag);
        });
    }
  });

  // Selecting newly created tab.
  v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

  // Adding unique names to spans.
  var v_tab_title_span = document.getElementById('tab_title');
  v_tab_title_span.id = 'tab_title_' + v_tab.id;
  var v_tab_loading_span = document.getElementById('tab_loading');
  v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
  var v_tab_check_span = document.getElementById('tab_check');
  v_tab_check_span.id = 'tab_check_' + v_tab.id;

  // Creating the template for the inner_debugger_tab.
  var v_html =
  '<div id="txt_func_body_' + v_tab.id + '" style="width: 100%; height: 200px; border: 1px solid #c3c3c3;"></div>' +
  '<div class="omnidb__resize-line__container--horizontal" onmousedown="resizeVertical(event)">' +
    '<div class="resize_line_horizontal"></div><div style="height:5px;"></div>' +
  '</div>' +
  "<div class='row mb-1'>" +
    "<div class='tab_actions omnidb__tab-actions col-12'>" +
      '<button id="bt_start_' + v_tab.id + '" class="btn btn-sm btn-primary omnidb__tab-actions__btn" title="Start" onclick="startDebug();"><i class="fas fa-bolt fa-light"></i></button>' +
      '<button id="bt_reload_' + v_tab.id + '" class="btn btn-sm btn-secondary omnidb__tab-actions__btn" title="Reload Function Attributes"><i class="fas fa-sync-alt fa-light"></i></button>' +
      '<button id="bt_step_over_' + v_tab.id + '" class="btn btn-sm btn-secondary omnidb__tab-actions__btn" title="Step Over (Next Statement)" style="display: none;" onclick="stepDebug(0);"><i class="fas fa-angle-right fa-light"></i></button>' +
      '<button id="bt_step_out_' + v_tab.id + '" class="btn btn-sm btn-secondary omnidb__tab-actions__btn" title="Resume (Next Breakpoint)" style="display: none;" onclick="stepDebug(1);"><i class="fas fa-angle-double-right fa-light"></i></button>' +
      '<button id="bt_cancel_' + v_tab.id + '" class="btn btn-sm btn-danger omnidb__tab-actions__btn" title="Cancel" style="display: none; vertical-align: middle;" onclick="cancelDebug();">Cancel</button>' +
      // '<div id="div_debug_info_' + v_tab.id + '" class="query_info" style="display: inline-block; margin-left: 5px; vertical-align: middle;"></div>' +

      '<div id="div_debug_info_' + v_tab.id + '" class="omnidb__query-info"></div>' +
    "</div>" +
  "</div>" +
  "<div id='debug_result_tabs_container" + v_tab.id + "' class='omnidb__query-result-tabs'>" +
    "<button style='position:absolute;top:0.25rem;right:0.25rem;' type='button' class='btn btn-sm btn-icon' onclick=toggleExpandToPanelView('debug_result_tabs_container" + v_tab.id + "')><i class='fas fa-expand'></i></button>" +
    "<div id='debug_result_tabs_" + v_tab.id + "'>" +
    "</div>" +
  "</div>";

  // Updating the html.
  v_tab.elementDiv.innerHTML = v_html;

  // Creating tab list at the bottom of the query tab.
  var v_curr_tabs = createTabControl({ p_div: 'debug_result_tabs_' + v_tab.id });

  // Tab selection callback for `parameter` tab.
  var v_selectParameterTabFunc = function() {
    v_curr_tabs.selectTabIndex(0);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDebugTab = 'parameter';
    v_tab.tag.resize();
  }

  // Tab selection callback for `variable` tab.
  var v_selectVariableTabFunc = function() {
    v_curr_tabs.selectTabIndex(1);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDebugTab = 'variable';
    v_tab.tag.resize();
  }

  // Tab selection callback for `result` tab.
  var v_selectResultTabFunc = function() {
    v_curr_tabs.selectTabIndex(2);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDebugTab = 'result';
    v_tab.tag.resize();
  }

  // Tab selection callback for `message` tab.
  var v_selectMessageTabFunc = function() {
    v_curr_tabs.selectTabIndex(3);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDebugTab = 'message';
    v_tag.div_count_notices.style.display = 'none';
    v_tab.tag.resize();
  }

  // Tab selection callback for `statistics` tab.
  var v_selectStatisticsTabFunc = function() {
    v_curr_tabs.selectTabIndex(4);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDebugTab = 'statistics';
    v_tag.div_count_notices.style.display = 'none';
    v_tab.tag.resize();
  }

  // Creating the `parameter` tab.
  var v_parameter_tab = v_curr_tabs.createTab({
    p_name: 'Parameter',
    p_close: false,
    p_clickFunction: function(e) {
      v_selectParameterTabFunc();
    }
  });
  v_parameter_tab.elementDiv.innerHTML =
  '<div class="p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary">' +
    '<div id="div_parameters_' + v_tab.id + '" class="omnidb__query-result-tabs__content" style="width: 100%; overflow: hidden;"></div>' +
  '</div>';

  // Creating the `variable` tab.
  var v_variable_tab = v_curr_tabs.createTab({
    p_name: 'Variable',
    p_close: false,
    p_clickFunction: function(e) {
      v_selectVariableTabFunc();
    }
  });
  v_variable_tab.elementDiv.innerHTML =
  '<div class="p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary">' +
    '<div id="div_variables_' + v_tab.id + '" class="omnidb__query-result-tabs__content" style="width: 100%; overflow: hidden;"></div>' +
  '</div>';

  // Creating the `result` tab.
  var v_result_tab = v_curr_tabs.createTab({
    p_name: 'Result',
    p_close: false,
    p_clickFunction: function(e) {
      v_selectResultTabFunc();
    }
  });
  v_result_tab.elementDiv.innerHTML =
  '<div class="p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary">' +
    '<div id="div_result_' + v_tab.id + '" class="omnidb__query-result-tabs__content" style="width: 100%; overflow: hidden;"></div>' +
  '</div>';

  // Creating the `message` tab.
  var v_message_tab = v_curr_tabs.createTab({
    p_name: 'Messages <div id="debug_result_tabs_count_notices_' + v_tab.id + '" class="count_notices" style="display: none;"></div>',
    p_close: false,
    p_clickFunction: function(e) {
      v_selectMessageTabFunc();
    }
  });
  v_message_tab.elementDiv.innerHTML =
  '<div class="p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary">' +
    '<div id="div_notices_' + v_tab.id + '" class="omnidb__query-result-tabs__content" style="width: 100%; overflow: hidden;"></div>' +
  '</div>';

  // Creating the `statistics` tab.
  var v_statistics_tab = v_curr_tabs .createTab({
    p_name: "Statistics",
    p_close: false,
    p_clickFunction: function(e) {
      v_selectStatisticsTabFunc();
    }
  });
  v_statistics_tab.elementDiv.innerHTML =
  '<div class="p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary">' +
    '<div id="div_statistics_' + v_tab.id + '" class="omnidb__query-result-tabs__content" style="width: 100%; overflow-x: auto; overflow-y: hidden;">' +
      '<div id="div_statistics_container_' + v_tab.id + '" style="height: 100%; position: relative;">' +
        '<canvas id="div_statistics_canvas_' + v_tab.id + '"></canvas>' +
      '</div>' +
    '</div>' +
  '</div>';

  // Creating the editor for `query`.
  var langTools = ace.require("ace/ext/language_tools");
  var v_editor = ace.edit('txt_func_body_' + v_tab.id);
  v_editor.$blockScrolling = Infinity;
  v_editor.setTheme("ace/theme/" + v_editor_theme);
  v_editor.session.setMode("ace/mode/sql");
  v_editor.setFontSize(Number(v_font_size));
  v_editor.setOptions({
    readOnly: true,
  });

  // Setting custom keyboard shortcuts callbacks.
  // $('#txt_func_body_' + v_tab.id).find('.ace_text-input').on('keyup',function(event){
  //   autocomplete_start(v_editor,0, event);
  // });
  // $('#txt_func_body_' + v_tab.id).find('.ace_text-input').on('keydown',function(event){
  //   autocomplete_keydown(v_editor, event);
  // });
  //
  // document.getElementById('txt_func_body_' + v_tab.id).addEventListener('contextmenu',function(event) {
  //   event.stopPropagation();
  //   event.preventDefault();
  //
  //   var v_option_list = [
  //     {
  //       text: 'Copy',
  //       icon: 'fas fa-terminal',
  //       action: function() {
  //         // Getting the value
  //         var copy_text = v_editor.getValue();
  //         // Calling copy to clipboard.
  //         uiCopyTextToClipboard(copy_text);
  //       }
  //     },
  //     {
  //       text: 'Save as snippet',
  //       icon: 'fas fa-save',
  //       submenu: {
  //         elements: buildSnippetContextMenuObjects('save', v_connTabControl.tag.globalSnippets, v_editor)
  //       }
  //     }
  //   ];
  //
  //   if (v_connTabControl.tag.globalSnippets.files.length != 0 || v_connTabControl.tag.globalSnippets.folders.length != 0)
  //     v_option_list.push(
  //       {
  //         text: 'Use snippet',
  //         icon: 'fas fa-book',
  //         submenu: {
  //           elements: buildSnippetContextMenuObjects('load', v_connTabControl.tag.globalSnippets, v_editor)
  //         }
  //       }
  //     )
  //   customMenu(
  //     {
  //       x:event.clientX+5,
  //       y:event.clientY+5
  //     },
  //     v_option_list,
  //     null
  //   );
  // });


  // Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
  v_editor.commands.bindKey("ctrl-space", null);
  v_editor.commands.bindKey("Cmd-,", null);
  v_editor.commands.bindKey("Ctrl-,", null);
  v_editor.commands.bindKey("Cmd-Delete", null);
  v_editor.commands.bindKey("Ctrl-Delete", null);
  v_editor.commands.bindKey("Ctrl-Up", null);
  v_editor.commands.bindKey("Ctrl-Down", null);
  v_editor.commands.bindKey("Up", null);
  v_editor.commands.bindKey("Down", null);
  v_editor.commands.bindKey("Tab", null);

  // Setting the autofocus for the editor component.
  document.getElementById('txt_func_body_' + v_tab.id).onclick = function() {
    v_editor.focus();
  };

  var v_resizeFunction = function () {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    if (v_tab_tag.currDebugTab) {
      v_tab_tag.editor.resize();
      if (v_tab_tag.currDebugTab=='variable') {
        v_tab_tag.div_variable.style.height = window.innerHeight - $(v_tab_tag.div_variable).offset().top - (1.25)*v_font_size + 'px';
        if (v_tab_tag.htVariable!=null)
        v_tab_tag.htVariable.render();
      }
      else if (v_tab_tag.currDebugTab=='parameter') {
        v_tab_tag.div_parameter.style.height = window.innerHeight - $(v_tab_tag.div_parameter).offset().top - (1.25)*v_font_size + 'px';
        if (v_tab_tag.htParameter!=null)
        v_tab_tag.htParameter.render();
      }
      else if (v_tab_tag.currDebugTab=='result') {
        v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - (1.25)*v_font_size + 'px';
        if (v_tab_tag.htResult!=null)
        v_tab_tag.htResult.render();
      }
      else if (v_tab_tag.currDebugTab=='message') {
        v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - (1.25)*v_font_size + 'px';
      }
      else if (v_tab_tag.currDebugTab=='statistics') {
        v_tab_tag.div_statistics.style.height = window.innerHeight - $(v_tab_tag.div_statistics).offset().top - (1.25)*v_font_size + 'px';
        if (v_tab_tag.chart!=null)
        v_tab_tag.chart.update();
      }
    }
  }

  // Setting all tab_tag params.
  var v_tag = {
    tab_id: v_tab.id,
    mode: 'debug',
    editor: v_editor,
    editorDivId: 'txt_func_body_' + v_tab.id,
    debug_info: document.getElementById('div_debug_info_' + v_tab.id),
    div_parameter: document.getElementById('div_parameters_' + v_tab.id),
    div_variable: document.getElementById('div_variables_' + v_tab.id),
    div_result: document.getElementById('div_result_' + v_tab.id),
    div_notices: document.getElementById('div_notices_' + v_tab.id),
    div_statistics: document.getElementById('div_statistics_' + v_tab.id),
    div_statistics_container: document.getElementById('div_statistics_container_' + v_tab.id),
    div_statistics_canvas: document.getElementById('div_statistics_canvas_' + v_tab.id),
    div_count_notices: document.getElementById('debug_result_tabs_count_notices_' + v_tab.id),
    tab_title_span : v_tab_title_span,
    tab_loading_span : v_tab_loading_span,
    tab_check_span : v_tab_check_span,
    bt_reload: document.getElementById('bt_reload_' + v_tab.id),
    bt_start: document.getElementById('bt_start_' + v_tab.id),
    bt_step_over: document.getElementById('bt_step_over_' + v_tab.id),
    bt_step_out: document.getElementById('bt_step_out_' + v_tab.id),
    bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
    state : 0,
    hasDataToRender: false,
    context: null,
    resize: v_resizeFunction,
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    queryTabControl: v_curr_tabs,
    currDebugTab: null,
    connTab: v_connTabControl.selectedTab,
    currDatabaseIndex: null,
    // tab_db_id: v_tab_db_id,
    markerId: null,
    markerList: [],
    htParameter: null,
    htVariable: null,
    htResult: null,
    chart: null,
    breakPoint: null
  };

  // Setting the v_tab_tag.
  v_tab.tag = v_tag;
  v_tag.selectParameterTabFunc = v_selectParameterTabFunc;
  v_tag.selectVariableTabFunc = v_selectVariableTabFunc;
  v_tag.selectResultTabFunc = v_selectResultTabFunc;
  v_tag.selectMessageTabFunc = v_selectMessageTabFunc;
  v_tag.selectStatisticsTabFunc = v_selectStatisticsTabFunc;

  //Customize editor to enable adding breakpoints
	//Creating breakpoint options
	$('#' + v_tab.tag.editorDivId).children('.ace_gutter').each(function () {
	    var v_gutter = $(this);
			v_gutter.css('cursor', 'pointer');
			v_gutter.click(function() {
				v_tab.tag.editor.session.selection.clearSelection();

				var v_row = v_tab.tag.editor.getSelectionRange().start.row;
				if (v_tab.tag.breakPoint == v_row)
					v_tab.tag.breakPoint = null;
				else
					v_tab.tag.breakPoint = v_row;

				v_tab.tag.editor.getSession().setAnnotations([{
					row: v_tab.tag.breakPoint,
					column: 0,
					text: "Breakpoint",
					type: "warning"
				}]);
			});
	});

  // Selecting the `parameter` tab by default.
  v_selectParameterTabFunc();

  // Creating `Add` tab in the `inner_query` tab list
  var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_name: '+',
    p_close: false,
    p_isDraggable: false,
    p_selectable: false,
    p_clickFunction: function(e) {
      showMenuNewTab(e);
    }
  });
  v_add_tab.tag = {
    mode: 'add'
  }

  // Requesting an update on the workspace layout and sizes.
  setTimeout(function() {
    v_resizeFunction();
  },10);

  v_editor.focus();
}
