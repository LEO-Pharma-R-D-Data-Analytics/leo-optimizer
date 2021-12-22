OPTIMIZED_PAYLOAD = """
query Query {
    allCitiesOptimized {
        state {
            country {
            continent {
                name
            }
            }
        }
        mayor {
            city {
                name
            }
        }
        district {
            city {
                mayor {
                    city {
                        district {
                            name
                        }
                    }
                }
            }
        }
    }
}
"""

NOT_OPTIMIZED_PAYLOAD = """
query Query {
    allCitiesNotOptimized {
        state {
            country {
            continent {
                name
            }
            }
        }
        mayor {
            city {
                name
            }
        }
        district {
            city {
                mayor {
                    city {
                        district {
                            name
                        }
                    }
                }
            }
        }
    }
}
"""