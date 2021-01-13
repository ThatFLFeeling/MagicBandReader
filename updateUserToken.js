'use strict';
'use AWS.DynamoDB';

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
//Enter your DynamoDB table name that stores tokens
var table = "";
//User ID you want to update token for
var User_ID = ;


exports.handler = function(event, context, callback) {

  var params = {
      TableName: table,
      Key:{
        "Column name that stores user ID in 'table' ": User_ID
    },
    //Column names for access token and refresh token
    UpdateExpression: "SET access_token_column_name = :a, refresh_token_column_name = :r",
    ExpressionAttributeValues:{
        ":a": a,
        ":r": r
    }
  };
  
  docClient.update(params, function(err, data) {
      callback(err, data);
      
  });
};