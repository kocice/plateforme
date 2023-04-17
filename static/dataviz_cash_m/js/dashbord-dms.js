/* jshint esversion: 6 */

function separateurMillier(nombre) {
    'use strict';
    return nombre.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function getCookie(name) {
  'use strict';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
      }
    }
  }
  return cookieValue;
}


// =====================================================================================================================

var defaultCols = {
  resizable: true,
  editable: false,
  sortable: true
};

//===================== Fin du Tableau =====================
// var initialData = JSON.parse("{{data|escapejs}}");
const columnDefsData = [
  {field: 'produits', width: 145, pinned: 'left'},
  {field: 'abonné', width: 100, type: 'numericColumn'},
  {headerName: 'Taux', field: 'equipement', width: 100, type: 'numericColumn'},
  {headerName: 'Abonnés E', field: 'abonné_encours', width: 120, type: 'numericColumn'},
  {headerName: 'Taux E', field: 'equipement_encours', width: 100, type: 'numericColumn'},
  {headerName: 'TC M-1', field: 'tc_m1', width: 120, type: 'numericColumn', cellClassRules: cellClassRules},
  {headerName: 'TC N-1', field: 'tc_n1', width: 120, type: 'numericColumn', cellClassRules: cellClassRules},
];

const gridOptionsData = {
  defaultColDef: defaultCols,
  rowClassRules: {
    'row-table': function (params) {
      return params.data.equipement >= 0;
    },
  },
  getRowStyle: params => {
    if (params.node.rowIndex % 2 === 0) {
      return {background: '#eee'};
    }
  },
  rowHeight: 40,
  columnDefs: columnDefsData,
  rowData: initialData
};

document.addEventListener('DOMContentLoaded', function() {
    var gridDiv = document.querySelector('#data');
    new agGrid.Grid(gridDiv, gridOptionsData);
});
//===================== Fin du Tableau =====================


  //===================== Resumé des infos sur le produit =================================
  // var initialInfoProd = JSON.parse("{{info_prod|escapejs}}");
const columnDefsInfoProd = [
  {field: 'Abonne', width: 100, type: 'numericColumn'},
  {headerName: 'Cible Corpo', field: 'Cible', width: 120, type: 'numericColumn'},
  {headerName: 'Abonnés Corpo', field: 'corpo_abonne', width: 140, type: 'numericColumn'},
  {headerName: '% Taux', field: 'Equipement', width: 94, type: 'numericColumn', cellClassRules: cellClassRulesProd},
];

const gridOptionsInfoProd = {
  defaultColDef: {
    resizable: true,
    editable: false,
    sortable: true
  },
  rowClassRules: {
    'row-prod': function (params) {
      return params.data.Equipement >= 0;
    },
  },
  //rowHeight: 100,
  columnDefs: columnDefsInfoProd,
  rowData: initialInfoProd
};

document.addEventListener('DOMContentLoaded', function() {
    var gridDiv = document.querySelector('#infoProd');
    new agGrid.Grid(gridDiv, gridOptionsInfoProd);
  });
  // ========================== End Resumé Info Produits =========================


  //===================== Resumé des infos sur les Gestionnaires =================
// var initialGest = JSON.parse("{{info_ges|escapejs}}");
const columnDefsGest = [
  {
    field: 'Gestionnaires',
    width: 194,
    pinned: 'left',
    filter: 'agTextColumnFilter',
    floatingFilter: true,
    sortable: false
  },
  {field: 'Cible', width: 90, type: 'numericColumn', cellClassRules: cellClassRulesNormale},
  {field: 'Abonnés', width: 100, type: 'numericColumn', cellClassRules: cellClassRulesNormale},
  {headerName: '% Taux', field: 'Equipement', width: 95, type: 'numericColumn', cellClassRules: cellClassRules},
];
const gridOptionsGest = {
  defaultColDef: {
    resizable: true,
    editable: false,
    sortable: true
  },
  getRowStyle: params => {
    if (params.node.rowIndex % 2 === 0) {
      return {background: '#eee'};
    }
  },

  rowHeight: 20,
  columnDefs: columnDefsGest,
  rowData: initialGest
};
document.addEventListener('DOMContentLoaded', function() {
  const gridDiv = document.querySelector('#gest');
  new agGrid.Grid(gridDiv, gridOptionsGest);
  });
// ========================== End Resumé Info Produits =========================


//===================== Clients non Abonnés ==============================
// var initialNonAb = JSON.parse("{{info_non_ab|escapejs}}");
const columnDefsNonAb = [
  {field: 'Racine', pinned: 'left', filter: false, width: 100},
  {headerName: 'Client', field: 'Nom_client', pinned: 'left', floatingFilter: true, width: 230},
  {headerName: 'Date de Création', field: 'Contact_date', width: 170},
  {headerName: 'Description', field: 'Secteur', width: 190},
  {field: 'Ciblé', width: 100},
  {headerName: 'Gestionnaire', floatingFilter: true, field: 'Nom_gestionnaire', width: 185},
  {field: 'Services', floatingFilter: true, width: 120},
  {field: 'Directions', floatingFilter: true, width: 130},
  {field: 'Agence', width: 250},
];
const gridOptionsNonAb = {
  defaultColDef: {
    resizable: true,
    editable: false,
    filter: 'agTextColumnFilter',
  },
  pagination: true,
  paginationPageSize: 10,
  getRowStyle: params => {
    if (params.node.rowIndex % 2 === 0) {
      return {background: '#eee'};
    }
  },
  rowHeight: 23,
  columnDefs: columnDefsNonAb,
  rowData: initialNonAb,
  groupDisplayType: 'groupRows',
};
document.addEventListener('DOMContentLoaded', function() {
  var gridDiv = document.querySelector('#nonAb');
  new agGrid.Grid(gridDiv, gridOptionsNonAb);
});
//===================== End Clients non Abonnés =========================


//===================== Statistique par direction ==============================
  // var initialresum = JSON.parse("{{resum_direction|escapejs}}");
const columnDefsResum = [
  {field: 'Directions', pinned: 'left', filter: false, width: 110, sortable: false},
  {field: 'Services', pinned: 'left', width: 105, sortable: false},
  {field: "Portefeuille", width: 120, type: 'numericColumn', cellClassRules: cellClassRulesNormale},
  {field: "Cible", width: 90, type: 'numericColumn', cellClassRules: cellClassRulesNormale},
  {field: "Abonnés", width: 100, type: 'numericColumn', cellClassRules: cellClassRulesNormale},
  //{field: "Non Abonnés", width: 130, type: 'numericColumn', cellClassRules: cellClassRulesNormale},
  {headerName: "% Taux", field: "Equipement", width: 100, type: 'numericColumn', cellClassRules: cellClassRules},
];

var gridOptionsResum = {
    defaultColDef: {
      resizable: true,
      editable: false,
      sortable: true
    },
    getRowStyle: params => {
      if (params.node.rowIndex % 2 === 0) {
          return { background: '#eee' };
      }
    },
    rowHeight: 34,
    columnDefs: columnDefsResum,
    rowData: initialresum
  };

  document.addEventListener('DOMContentLoaded', function() {
    var gridDiv = document.querySelector('#resum');
    new agGrid.Grid(gridDiv, gridOptionsResum);
  });
  //===================== End Directon =========================

// =====================================================================================================================

document.addEventListener('DOMContentLoaded', () => {
  'use strict';
  const gridDivLigneCredit = document.querySelector('#grid-credit');
  new agGrid.Grid(gridDivLigneCredit, gridOptionsLigneCredit);
});

function onBtnExport() {
  'use strict';
  var params = {
    columnSeparator: ';',
    fileName: 'Credit.csv' // nom du fichier de sortie
  };
  gridOptionsLigneCredit.api.exportDataAsCsv(params);
}


// =====================================================================================================================

function getData(method, args) {
  'use strict';

  const url = window.location.href;
  console.log(url);
  const body = JSON.stringify(args.body);

  fetch(url, {
    method: method,
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-Type': 'application/json',
      /* jshint ignore:start */
      'X-CSRFToken': getCookie('csrftoken')
      /* jshint ignore:end */
    },
    body: body,
  })
    .then(function (response) {
      if (response.ok) {
        // Récupération des données reçues
        return response.json();
      } else {
        // Gestion d'une erreur de requête
        throw new Error('Error while fetching data');
      }
    })
    .then(function (data) {
      // Utilisation des données reçues
      /* jshint ignore:start */
      console.log(data);
      /* jshint ignore:end */
      // ===============================================================================================================
      let sommeCredit = 0;
      if (typeof data.data !== 'undefined') {
        for (let i = 0; i < data.data.length; i++) {
          sommeCredit = sommeCredit + data.data[i].montant;
        }
        document.getElementById(`somme-credit`).innerHTML = `${separateurMillier(sommeCredit.toFixed(0))} FCFA`;

        gridOptionsLigneCredit.api.setRowData(data.data);
      }
    })
    .catch(function (error) {
      // Gestion d'une erreur de requête
      /* jshint ignore:start */
      console.error(error);
      /* jshint ignore:end */
    });
}


// =====================================================================================================================
document.addEventListener('DOMContentLoaded', function() {
  'use strict';
  getData('POST',{
    body: {
      test: 'hello',
    },
  });
});


document.getElementById('patch-button').addEventListener('click', function() {

  getData('PUT',{
      body: {
        id: document.getElementById('ligne-credit-id').value,
        montant: document.getElementById('montant').value,
        commentaire: document.getElementById('commentaire').value,
        typeCredit: document.getElementById('type-credit').value
      },
  });

  // Fermer le modal
  $('#modal-edit-ligne-credit').modal('hide');
});