Check the repo README (review section) to see how to use this checklist.

- [ ] Integration merged into API branch?

### Customer experience review
- [ ] Can this API be deployed locally, and then accessed (aka does it work)?
- [ ] Documentation
  - [ ] Is it clear from the documentation what this API does?
  - [ ] Is the documentation clear and understandable?
  - [ ] Is the English correct, grammar, spelling, choice of words?
  - [ ] Do the examples work as expected?
- [ ] Does the API functionality align with it's name (URL)?
- [ ] Does the choice of functionality make sense (does it do too little, just enough or too much)?
- [ ] Are all relevant use cases, positive and negative, covered (are there too few, just enough or too many use cases covered)?
- [ ] Does the data model (schema, responses, request parameters, request body) make sense? Is it consistent with okapi?
- [ ] Errors
  - [ ] In case a negative use case responds with anything other than 2xx, does the error and it's message make sense?
  - [ ] Is the API unbreakable, i.e., never throws 500s?

### API design review
- [ ] Is the directory structure correct?
- [ ] Is file and directory naming according to conventions?
- [ ] Are the `__init__.py` files in place correctly?
- [ ] Does the YAML file pass validation?
- [ ] In case this API stores data, is the RAML file present and correct?

### Code review
- [ ] Does the code do what it is supposed to?
- [ ] Is the code easy to read and understand?
- [ ] Does the code conform to PEP 8 (check PyCharm inspections - maybe CTRL+ALT+L)?
- [ ] Do PyCharm inspections report any other problems that need fixing?
- [ ] Do you have any comments on the code? Please report in the PR comments before approving.