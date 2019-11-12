import path from 'path'
import fs from 'fs'
import express from 'express'
import bodyParser from 'body-parser'
import packageJson from '../package.json'

import { ClassificationResult } from "src/models"
import { AdaptationEndpoint } from "./environment"
import { post } from "./utils"
import { Search } from "./search"
import { Wiki} from "./wiki"

/** Express application instance */
const app: express.Application = express()

/** Search module */
const search = new Search()

/** Wiki module */
const wiki = new Wiki()

// Encode json bodies in requests
app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

// Error handler
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  if (err) {
    console.error("-----------------ERR-----------------")
    console.error(err.message, err.stack)
    console.error("----------------END-ERR---------------")
    return res.json({ message: err.message, stack: err.stack })
  }
  next()
})

// Index entry-point 
app.get("/", (req, res) => res.json({ message: `App version ${packageJson.version}.` }))

// Docs entry-point
app.use("/docs", express.static(path.join(__dirname, '../docs')))

// Main entry-point
app.post('/', async (req, res) => {

  try {
    console.log(`[App.ts] Post request received`);

    /** Parsed Classification result */
    const classificationResult = req.body as ClassificationResult
    if (!classificationResult) {
      return res.json({
        message: "Missing required body."
      })
    }

    /** Page Result array */
    const results = await Promise.all([
      search.search(classificationResult),
      wiki.search(classificationResult)
    ]).then(allResults => [].concat(...allResults))

    console.log(`[App.ts] Google and Wikipedia requests ended`);

    // Call adaptation for summary
    return post(AdaptationEndpoint + "/tailored_text", {
      userProfile: classificationResult.userProfile,
      results: results
    }).then(r => res.send(r)) // respond with the obtained object

    // Catch any error and inform the caller
  } catch (ex) {
    console.log({ message: ex.message, stack: ex.stack })
    return res.json({ message: ex.message, stack: ex.stack })
  }

})

export default app
