// /* jshint esversion: 6 */
//
// function separateurMillier(nombre) {
//     'use strict';
//     return nombre.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
// }
//
// function getCookie(name) {
//   'use strict';
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//     const cookies = document.cookie.split(';');
//     for (let i = 0; i < cookies.length; i++) {
//       const cookie = cookies[i].trim();
//       // Does this cookie string begin with the name we want?
//         if (cookie.substring(0, name.length + 1) === (name + '=')) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//       }
//     }
//   }
//   return cookieValue;
// }
//
// // =====================================================================================================================
// let defaultCol = {
//   resizable: true,
//   flex: 1
// };
//
// const colLigneCredit = [
//   {
//     headerName: '#',
//     field: 'num_ligne_credit',
//     maxWidth: 70,
//     sortable: true,
//   },
//   {
//     field: 'id',
//     maxWidth: 70,
//     suppressColumnsToolPanel: true,
//   },
//   {
//     headerName: 'Date',
//     field: 'date_demande',
//     maxWidth: 190,
//     sortable: true,
//   },
//   {
//     headerName: 'Type de crédit',
//     field: 'type_credit',
//     sortable: true,
//   },
//   {
//     headerName: 'Montant ( XOF )',
//     field: 'montant',
//     type: 'numericColumn',
//     sortable: true,
//     valueFormatter: function(params) {
//       'use strict';
//       return params.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
//     }
//   },
//   {
//     headerName: 'Commentaire',
//     field: 'commentaire',
//     editable: true,
//   },
//   {
//     headerName: '',
//     field: 'supprimer',
//     maxWidth: 80,
//     cellRenderer: function(params) {
//       const deleteButton = document.createElement('button');
//       deleteButton.innerHTML = '<i class="fa fa-trash"></i>';
//       deleteButton.className = 'btn btn-danger shadow btn-xs sharp sweet-success-cancel';
//
//       // Fonction exécutée lorsqu'on clique sur le bouton de suppression
//       deleteButton.addEventListener('click', function() {
//         Swal.fire({
//           text: 'Êtes-vous sûr de vouloir supprimer cette ligne ?',
//           icon: 'warning',
//           showCancelButton: true,
//           confirmButtonColor: '#dc3545',
//           cancelButtonColor: '#6c757d',
//           confirmButtonText: 'Oui, supprimer',
//           cancelButtonText: 'Annuler'
//         }).then((result) => {
//           if (result.value) {
//             const selectedRow = params.data;
//             params.api.applyTransaction({ remove: [selectedRow] });
//             // Supprimer la ligne de la base de données
//             console.log(selectedRow);
//             getData('DELETE',{
//               body: {
//                 data: selectedRow,
//               },
//             });
//           }
//         });
//       });
//
//       const editButton = document.createElement('button');
//       editButton.innerHTML = '<i class="fa fa-pencil"></i>';
//       editButton.className = 'btn btn-primary shadow btn-xs sharp me-1';
//       editButton.setAttribute('data-bs-toggle', 'modal');
//       editButton.setAttribute('data-bs-target', '.bd-example-modal-lg');
//
//       editButton.addEventListener('click', function() {
//         document.getElementById('ligne-credit-id').value = params.data.id;
//         document.getElementById('montant').value = params.data.montant;
//         document.getElementById('commentaire').value = params.data.commentaire;
//         // for (var i = 0; i < typeCredit.options.length; i++) {
//         //   if (typeCredit.options[i].value === params.data.type_credit) {
//         //       typeCredit.selectedIndex = i;
//         //       break;
//         //   }
//         // }
//       });
//
//       const buttonsContainer = document.createElement('div');
//       buttonsContainer.className = 'sweetalert d-flex';
//       buttonsContainer.appendChild(editButton);
//       buttonsContainer.appendChild(deleteButton);
//
//       return buttonsContainer;
//     }
//   }
// ];
//
// const gridOptionsLigneCredit = {
//   columnDefs: colLigneCredit,
//   rowClass: 'custom',
//   rowHeight: 35,
//   paginationPageSize: 10,
//   pagination: true,
//   defaultColDef: defaultCol,
//   getRowStyle: params => {
//     'use strict';
//     if (params.node.rowIndex % 2 === 0) {
//       return { background: '#eee' };
//     }
//   },
// };
//
// document.addEventListener('DOMContentLoaded', () => {
//   'use strict';
//   const gridDivLigneCredit = document.querySelector('#grid-credit');
//   new agGrid.Grid(gridDivLigneCredit, gridOptionsLigneCredit);
// });
//
// function onBtnExport() {
//   'use strict';
//   var params = {
//     columnSeparator: ';',
//     fileName: 'Credit.csv' // nom du fichier de sortie
//   };
//   gridOptionsLigneCredit.api.exportDataAsCsv(params);
// }
//
//
// // =====================================================================================================================
//
// function getData(method, args) {
//   'use strict';
//
//   const url = window.location.href;
//   console.log(url);
//   const body = JSON.stringify(args.body);
//
//   fetch(url, {
//     method: method,
//     headers: {
//       'Accept': 'application/json, text/plain, */*',
//       'Content-Type': 'application/json',
//       /* jshint ignore:start */
//       'X-CSRFToken': getCookie('csrftoken')
//       /* jshint ignore:end */
//     },
//     body: body,
//   })
//     .then(function (response) {
//       if (response.ok) {
//         // Récupération des données reçues
//         return response.json();
//       } else {
//         // Gestion d'une erreur de requête
//         throw new Error('Error while fetching data');
//       }
//     })
//     .then(function (data) {
//       // Utilisation des données reçues
//       /* jshint ignore:start */
//       console.log(data);
//       /* jshint ignore:end */
//       // ===============================================================================================================
//       let sommeCredit = 0;
//       if (typeof data.data !== 'undefined') {
//         for (let i = 0; i < data.data.length; i++) {
//           sommeCredit = sommeCredit + data.data[i].montant;
//         }
//         document.getElementById(`somme-credit`).innerHTML = `${separateurMillier(sommeCredit.toFixed(0))} FCFA`;
//
//         gridOptionsLigneCredit.api.setRowData(data.data);
//       }
//     })
//     .catch(function (error) {
//       // Gestion d'une erreur de requête
//       /* jshint ignore:start */
//       console.error(error);
//       /* jshint ignore:end */
//     });
// }
//
//
// // =====================================================================================================================
// document.addEventListener('DOMContentLoaded', function() {
//   'use strict';
//   getData('POST',{
//     body: {
//       test: 'hello',
//     },
//   });
// });
//
//
// document.getElementById('patch-button').addEventListener('click', function() {
//
//   getData('PUT',{
//       body: {
//         id: document.getElementById('ligne-credit-id').value,
//         montant: document.getElementById('montant').value,
//         commentaire: document.getElementById('commentaire').value,
//         typeCredit: document.getElementById('type-credit').value
//       },
//   });
//
//   // Fermer le modal
//   $('#modal-edit-ligne-credit').modal('hide');
// });