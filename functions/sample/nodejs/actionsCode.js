// const { CloudantV1 } = require('@ibm-cloud/cloudant');
// const { IamAuthenticator } = require('ibm-cloud-sdk-core');
// var secrets = {
//     "COUCH_URL": "https://1f70d18e-2c41-41f7-9fe4-c7806acd9a8e-bluemix.cloudantnosqldb.appdomain.cloud",
//     "IAM_API_KEY": "kd1Cl515onirvb1ZB0B1a9mafZ8Ld1z1VyQ7CFYbvgcJ",
//     "COUCH_USERNAME": "1f70d18e-2c41-41f7-9fe4-c7806acd9a8e-bluemix"
// };

// function main(params) {

//     const authenticator = new IamAuthenticator({ apikey: secrets.IAM_API_KEY })
//     const cloudant = CloudantV1.newInstance({
//       authenticator: authenticator
//     });
//     cloudant.setServiceUrl(secrets.COUCH_URL);
    
//     if (params["state"]) {
//         var selector = { "state": params["state"] };
//         let matchedDealerships = getMatchingRecords(cloudant,"dealerships", selector);
//         return matchedDealerships;
//     } else {
//         let allDealerships = getAllRecords(cloudant, "dealerships");
//         return allDealerships;
//     }
    
// }

// /*
//  Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
//  eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
//  */
//  function getMatchingRecords(cloudant,dbname, selector) {
//      return new Promise((resolve, reject) => {
//          cloudant.postFind({db:dbname,selector:selector})
//                  .then((result)=>{
//                   resolve({result:result.result.docs});
//                  })
//                  .catch(err => {
//                     console.log(err);
//                      reject({ err: err });
//                  });
//           })
//  }
 
// function getAllRecords(cloudant,dbname) {
//     return new Promise((resolve, reject) => {
//         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
//             .then((result)=>{
//                 resolve({result:result.result.rows});
//             })
//             .catch(err => {
//                 console.log(err);
//                 reject({ err: err });
//             });
//     })
// }

function main(params) {
    // console.log(params);
    return new Promise(function (resolve, reject) {
        const { CloudantV1 } = require('@ibm-cloud/cloudant');
        const { IamAuthenticator } = require('ibm-cloud-sdk-core');
        const authenticator = new IamAuthenticator({ apikey: "kd1Cl515onirvb1ZB0B1a9mafZ8Ld1z1VyQ7CFYbvgcJ" })
        const cloudant = CloudantV1.newInstance({
            authenticator: authenticator
        });
        cloudant.setServiceUrl("https://1f70d18e-2c41-41f7-9fe4-c7806acd9a8e-bluemix.cloudantnosqldb.appdomain.cloud");
        if (params.st) {
            // return dealership with this state 
            cloudant.postFind({db:'dealerships',selector:{st:params.st}})
            .then((result)=>{
              // console.log(result.result.docs);
              let code = 200;
              if (result.result.docs.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.docs
              });
            }).catch((err)=>{
              reject(err);
            })
        } else if (params.id) {
            id = parseInt(params.dealerId)
            // return dealership with this state 
            cloudant.postFind({
              db: 'dealerships',
              selector: {
                id: parseInt(params.id)
              }
            })
            .then((result)=>{
              // console.log(result.result.docs);
              let code = 200;
              if (result.result.docs.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.docs
              });
            }).catch((err)=>{
              reject(err);
            })
        } else {
            // return all documents 
            cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })            
            .then((result)=>{
              // console.log(result.result.rows);
              let code = 200;
              if (result.result.rows.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.rows
              });
            }).catch((err)=>{
              reject(err);
            })
      }
    }
    )}