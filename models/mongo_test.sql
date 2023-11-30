use LUapp;
show collections; // Collections are like tables
//db.dropDatabase();

db.companies.find();

db.companies.findOne();

db.companies.find({}, {name: 1,similar_companies: 1});

// Get json with similar companies
db.companies.aggregate([
    {$addFields: {size_sim_comps: {$size: "$similar_companies"}}},
    {$match: {size_sim_comps: {$gt: 0}}},
    {$project: {name: 1, similar_companies: 1}}
])

// Get locations of a company
db.companies.aggregate([
    {$addFields: {size_loc: {$size: "$locations"}}},
    {$match: {size_loc: {$gt: 0}}},
    {$project: {name: 1, locations: 1, _id: 0}}
])