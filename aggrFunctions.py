def campaign_summary_pipeline(filter_by):
    pipeline = [
        {
            "$match":filter_by
        },
        {
            "$group": {
                "_id": {
                    "campaign_id":"$campaign_id",
                    "date":{
                        "month": { 
                            "$month": {
                                "$dateFromString":{
                                    "dateString":"$updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            }
                        },
                        "day": { 
                            "$dayOfMonth": {
                                "$dateFromString":{
                                    "dateString":"$updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            }
                        },
                        "year": { 
                            "$year": {
                                "$dateFromString":{
                                    "dateString":"$updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            } 
                        }
                    }
                },
                "total_leads": {
                    "$sum": 1
                },
                "calls_made": {
                    "$sum": {
                        "$cond": [{
                            "$ne": ["$status", "unactioned"]
                        }, 1, 0]
                    }
                },
                "call_time": {
                    "$sum": "$time_taken"
                },
                "time_taken": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$status", "completed"]
                        }, "$time_taken", 0]
                    }
                },
                "total_interested": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$interested", "interested"]
                        }, 1, 0]
                    }
                },
                "total_unactioned": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$status", "unactioned"]
                        }, 1, 0]
                    }
                },
                "total_connected": {
                    "$sum": {
                        "$cond": [{
                            "$in": ["$status", ["actioned", "completed"]]
                        }, 1, 0]
                    }
                }
            }
        }, 
        {
            "$project": {
                "campaign_id":"$_id.campaign_id",
                "entry_date":{
                    "$dateToString":{
                        "date":{
                            "$dateFromString":{
                                "format":"%Y-%m-%d",
                                "dateString":{
                                "$toString":{
                                    "$concat":[
                                        {
                                            "$toString":"$_id.date.year"
                                        },
                                        "-",
                                        {
                                            "$toString":"$_id.date.month"
                                        },
                                        "-",
                                        {
                                            "$toString":"$_id.date.day"
                                        }
                                    ]
                                }
                                }
                            }
                        },
                        "format":"%Y-%m-%d"
                    }
                },
                "total_leads": "$total_leads",
                "calls_made": "$calls_made",
                "call_time": "$call_time",
                "time_taken": "$time_taken",
                "total_interested": "$total_interested",
                "total_unactioned": "$total_unactioned",
                "total_connected": "$total_connected"
            }
        }
    ]
    return pipeline

def leads_interest_summary(filter_by):
    pipeline =  [
        {
            "$match":filter_by
        },
        {
            "$group": {
                "_id": "$campaign_id",
                "total_leads": {
                    "$sum": 1
                },
                "total_interested": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$interested", "interested"]
                        },1, 0]
                    }
                },
                "total_uninterested": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$interested", "not_interested"]
                        }, 1, 0]
                    }
                }
            }
        }, 
        {
            "$project": {
                "campaign_id": "$_id",
                "total_interested": "$total_interested",
                "total_uninterested": "$total_uninterested"
            }
        }
    ]
    return pipeline

def leads_total_summary(filter_by):
    pipeline =  [
        {
            "$group": {
                "_id": "$campaign_id",
                "total_leads": {
                    "$sum": {
                        "$numberInt": "1"
                    }
                },
                "remaining_leads": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$status", "unactioned"]
                        }, {
                            "$numberInt": "1"
                        }, {
                            "$numberInt": "0"
                        }]
                    }
                }
            }
        }, 
        {
            "$project": {
                "campaign_id": "$_id",
                "total_leads": "$total_leads",
                "remaining_leads": "$remaining_leads"
            }
        }
    ]
    return pipeline

def earnings_summary(company_filter = {}, campaign_filter = {}, lead_filter = {}):
    pipeline = [
        {
            "$match":company_filter
        },
        {
            "$lookup":{
                "from": "campaigns",
                "localField": "_id",
                "foreignField": "company_id",
                "as": "campaigns"
            }
        },
        {   
            "$unwind":{
                "path": "$campaigns"
            }
        },
        {
            "$match":campaign_filter
        },
        {
            "$lookup":{
                "from": "leads",
                "localField": "campaigns._id",
                "foreignField": "campaign_id",
                "as": "leads"
            }
        },
        {   
            "$unwind":{
                "path": "$leads"
            }
        },
        {
            "$match":lead_filter
        },
        {   
            "$unwind":{
                "path": "$leads.call_logs"
            }
        },
        {
            "$group": {
                "_id": {
                    "date":{
                        "month": { 
                            "$month": {
                                "$dateFromString":{
                                    "dateString":"$leads.call_logs.updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            }
                        },
                        "day": { 
                            "$dayOfMonth": {
                                "$dateFromString":{
                                    "dateString":"$leads.call_logs.updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            }
                        },
                        "year": { 
                            "$year": {
                                "$dateFromString":{
                                    "dateString":"$leads.call_logs.updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            } 
                        }
                    }
                },
                "call_time": {
                    "$sum": "$leads.call_logs.time_taken"
                },
                "time_taken": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$leads.status", "completed"]
                        }, {"$ceil":{"$divide": [ "$leads.time_taken", 60 ]}}, 0]
                    }
                },
                "cost": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$leads.status", "completed"]
                        }, 
                        {
                            "$multiply":[
                                {
                                    "$ceil":{
                                        "$divide": [ 
                                            "$leads.time_taken", 60 
                                        ]
                                    }
                                }, 
                                {"$toDouble":"$billing.charge_amount"}
                            ]
                        }, 0]
                    }
                }
            }
        }, 
        {
            "$project": {
                "entry_date":{
                    "$dateToString":{
                        "date":{
                            "$dateFromString":{
                                "format":"%Y-%m-%d",
                                "dateString":{
                                "$toString":{
                                    "$concat":[
                                        {
                                            "$toString":"$_id.date.year"
                                        },
                                        "-",
                                        {
                                            "$toString":"$_id.date.month"
                                        },
                                        "-",
                                        {
                                            "$toString":"$_id.date.day"
                                        }
                                    ]
                                }
                                }
                            }
                        },
                        "format":"%Y-%m-%d"
                    }
                },
                "call_time": "$call_time",
                "time_taken": "$time_taken",
                "cost": "$cost"
            }
        },
        { 
            "$sort": {
                "entry_date":1
            }
        }
    ]
    return pipeline

def earnings_summary_campaign(company_filter = {}, campaign_filter = {}, lead_filter = {}):
    pipeline = [
        {
            "$match":company_filter
        },
        {
            "$lookup":{
                "from": "campaigns",
                "localField": "_id",
                "foreignField": "company_id",
                "as": "campaigns"
            }
        },
        {   
            "$unwind":{
                "path": "$campaigns"
            }
        },
        {
            "$match":campaign_filter
        },
        {
            "$lookup":{
                "from": "leads",
                "localField": "campaigns._id",
                "foreignField": "campaign_id",
                "as": "leads"
            }
        },
        {   
            "$unwind":{
                "path": "$leads"
            }
        },
        {
            "$match":lead_filter
        },
        {   
            "$unwind":{
                "path": "$leads.call_logs"
            }
        },
        {
            "$group": {
                "_id": {
                    "date":{
                        "month": { 
                            "$month": {
                                "$dateFromString":{
                                    "dateString":"$leads.call_logs.updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            }
                        },
                        "day": { 
                            "$dayOfMonth": {
                                "$dateFromString":{
                                    "dateString":"$leads.call_logs.updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            }
                        },
                        "year": { 
                            "$year": {
                                "$dateFromString":{
                                    "dateString":"$leads.call_logs.updated_at",
                                    "format": "%Y-%m-%d %H:%M:%S"
                                }
                            } 
                        }
                    },
                    "campaign_id":"$campaigns._id"
                },
                "num_calls": {
                    "$sum": 1
                },
                "call_time": {
                    "$sum": "$leads.call_logs.time_taken"
                },
                "time_taken": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$leads.status", "completed"]
                        }, {"$ceil":{"$divide": [ "$leads.time_taken", 60 ]}}, 0]
                    }
                },
                "cost": {
                    "$sum": {
                        "$cond": [{
                            "$eq": ["$leads.status", "completed"]
                        }, 
                        {
                            "$multiply":[
                                {
                                    "$ceil":{
                                        "$divide": [ 
                                            "$leads.time_taken", 60 
                                        ]
                                    }
                                }, 
                                {"$toDouble":"$billing.charge_amount"}
                            ]
                        }, 0]
                    }
                }
            }
        }, 
        {
            "$project": {
                "entry_date":{
                    "$dateToString":{
                        "date":{
                            "$dateFromString":{
                                "format":"%Y-%m-%d",
                                "dateString":{
                                "$toString":{
                                    "$concat":[
                                        {
                                            "$toString":"$_id.date.year"
                                        },
                                        "-",
                                        {
                                            "$toString":"$_id.date.month"
                                        },
                                        "-",
                                        {
                                            "$toString":"$_id.date.day"
                                        }
                                    ]
                                }
                                }
                            }
                        },
                        "format":"%Y-%m-%d"
                    }
                },
                "campaign_id":"$_id.campaign_id",
                "call_time": "$call_time",
                "time_taken": "$time_taken",
                "cost": "$cost",
                "num_calls":"$num_calls"
            }
        },
        { 
            "$sort": {
                "entry_date":1
            }
        }
    ]
    return pipeline