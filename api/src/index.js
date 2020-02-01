const mongoose = require("mongoose");
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const escapeRegExp = require("lodash.escaperegexp");

mongoose.connect(
  process.env.MONGO_URL || "mongodb://root:root@localhost:27017/admin",
  { useNewUrlParser: true, useUnifiedTopology: true }
);

const PORT = process.env.PORT || 3000;
const app = express();
app.use(cors());
app.use(bodyParser.json());

/**
 * POST endpoint.
 *
 * Expects a JSON with the property `filter`, it queries the database
 * looking for the string in filter anywhere in the URL, title or text
 * of the pages and return all the results.
 *
 * TODO: implement pagination
 */
app.post("/api/v1.0.0/search", (req, res) => {
  const filter = escapeRegExp(req.body.filter);
  const filterRegex = RegExp(`.*${filter}.*`);

  mongoose.connection.db.collection("success_page", (error, collection) => {
    if (error) {
      res.send({ payload: [], error: "Error connecting to database" });
    } else {
      collection
        .find({
          $or: [
            { url: filterRegex },
            { title: filterRegex },
            { text: filterRegex }
          ]
        })
        .toArray((error, results) => {
          if (error) {
            res.send({ payload: [], error: "Error retrieving results" });
          } else {
            res.send({ payload: results, error: null });
          }
        });
    }
  });
});

app.listen(PORT, "0.0.0.0");
