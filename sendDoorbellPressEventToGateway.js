'use strict';
'use AWS.DynamoDB';

const https = require('https');
var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = function(request, context, callback) {
  var accessToken;
  //Add your client ID
  var client_id = '';
  //Add your client secret
  var client_secret = '';
  var params = {
    //DynamoDB table name where you store tokens
    TableName: "",
    //Column for user IDs and the user ID you want to modify
    Key: {
        "column name for user IDs": user ID you want to modify
    },
    //Add column names for access token, token timestamp, and the refresh token
    "ProjectionExpression": "access_token_column_name, token_timestamp_column_name, refresh_token_column_name"
  }

//check if token needs to be refreshed
docClient.scan(params, async function(err, data) { 
    callback(err, data);
    //Column name for the token timestamp
    var tokenTimestamp = data.Items[0].tokenTimestampColumnName;
    //Column name for the refresh token
    var refreshToken = data.Items[0].refreshTokenColumnName;
    
    if (Date.now() > tokenTimestamp + 3600000) {
      var body = '';
      var request =  new Promise((resolve, reject) => {
        const data = {
              grant_type: 'refresh_token',
              refresh_token: refreshToken,
              client_id: client_id,
              client_secret: client_secret
        };
      
          const options = {
            host: 'api.amazon.com',
            path: '/auth/o2/token',
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }
          };
      
          //create the request object with the callback with the result
          const req = https.request(options, (res) => {
              res.on('data', function (chunk) {
                  body += chunk;
              });
              res.on('end', function() {
                  resolve(body)
              });
          });
      
          // handle the possible errors
          req.on('error', (e) => {
            reject(e.message);
          });
      
          //do the request
          req.write(JSON.stringify(data));
          req.end();
      });
      
      await request
        .then(async result => {            
            await updateToken(result).then(data => {
                console.log("Got token db response:")
                console.log(data);
            });

        });
    }
  
});

  async function updateToken(result, response) {
      //DynamoDB table name where you store tokens
      var table = "";
      //The user ID you want to update token for
      var User_ID = ;
      var parsedResult = JSON.parse(result);
      
      var params = {
          TableName: table,
          Key: {
              //Column name for user IDs
              "column name for user IDs": User_ID 
          },
          //Column names for access token, refresh token, and token timestamp
          UpdateExpression: "set access_token_column = :a, refresh_token_column = :r, token_timestamp_column = :t",
          ExpressionAttributeValues:{
              ":a": parsedResult.access_token,
              ":r": parsedResult.refresh_token,
              ":t": Date.now()
          }
      };
      console.log("Params: " + JSON.stringify(params));
            
      return new Promise(function(resolve, reject) {
          docClient.update(params, function(err, data) {
              if(err) {
                  reject(err);
              }else if(data) {
                  resolve(data);
              }
          });
      });
  }

docClient.scan(params, function(err, data) {
            callback(err, data);
            //Column name for access token
            accessToken = data.Items[0].access_token_column_name;
    
            var body = '';
            var request =  new Promise((resolve, reject) => {
              const data = {
                "context": {},
                "event": {
                    "header": {
                        //Add desired message ID
                        "messageId": "",
                        "namespace" : "Alexa.DoorbellEventSource",
                        "name": "DoorbellPress",
                        "payloadVersion": "3"
                    },
                    "endpoint": {
                        "scope": {
                            "type": "BearerToken",
                            "token": accessToken
                        },
                        //Add desired endpoint ID
                        "endpointId": ""
                    },
                    "payload" : {
                        "cause": {
                            "type": "PHYSICAL_INTERACTION"
                        },
                        //Add timestamp
                        "timestamp": ""
                    }
                }
              };
            
                const options = {
                  host: 'api.amazonalexa.com',
                  path: '/v3/events',
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json'
                  }
                };
            
                //create the request object with the callback with the result
                const req = https.request(options, (res) => {
                    res.on('data', function (chunk) {
                        body += chunk;
                    });
                    res.on('end', function() {
                        resolve(body)
                    });
                });
            
                // handle the possible errors
                req.on('error', (e) => {
                  reject(e.message);
                });
            
                //do the request
                req.write(JSON.stringify(data));
                req.end();
            });
    
    });
};