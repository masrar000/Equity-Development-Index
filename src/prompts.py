rag_fusion_with_no_action = {
    "Project Description": [{
        "Affordable residential (low AMI - supportive)":
            '''
            How many units of Affordable Residential Low AMI supportive units are present with no action? Look for the values in RWCDS Summary table, if the table is present. 
            When answering, use this format:
            Format:
            Affordable residential (low AMI - supportive) With No Action: [number]
            ''',
        
        "Office Space":
            '''
            How much is the retail Gross square footage with No Action Condition for commercial land use?. When answering, use this format:
            Format:
            Total GSF With No Action: [number]
            ''',
        "Healthcare facilities":
            ''' 
            How many square feet of space is designated exclusively for healthcare facilities, such as hospitals, clinics, or medical offices, explicitly mentioned under the NO-ACTION CONDITION?
            When answering, use this format:
            Format: Healthcare facilities With No Action: [number]
            ''',
        "Community Space":
            '''
            How many gross square feet (GSF) of Community Facility Space is present under No Action Condition?
            When answering, use this format:
            Format: Community Space With No Action: [number]
            ''',
        "Cultural Space":
            '''
            How many square feet of space is designated exclusively for cultural facilities under the NO-ACTION CONDITION?
            When answering, use this format:
            Format: Cultural Space With No Action: [number]
            ''',
        "Affordable Residential (high AMI)":
            '''
            How many units of affordable residential greater than or equal to 80% AMI are present with no action condition? Total Affordable Units- Affordable units earning upto 80% of AMI = Affordable Residential (high AMI). 
            When answering, use this format:
            Format: Affordable Residential (high AMI) With No Action: [number]
            ''',
        "Parking Space":
            '''
            How many Parking Spaces are available in No-Action Condition? Focus only on the development Site/Buildings under the "No-Action" condition. Look for values in tables describing parking conditions specific to the No-Action scenario. Avoid total parking supply for the entire study area unless explicitly part of the No-Action condition. Parking Spaces With Action - Increment = Parking Space without action. If parking spaces are displaced or unavailable, reflect the adjusted value as zero.
            When answering, use this format:
            Format:
            Parking Space With No Action: [number]
            ''',
        "Market Rate Residential":
            '''
            What is the total number of occupied Dwelling Units (DU) present specifically under No‐Action Condition, in table mentioning Increment, for Residential Land Use? All values are explicitly in a table. This value is also known as Total Dwelling Units (DU) or approximately how many DUs?
            When answering, use this format:
            Format: Market Rate With No Action: [number]
            ''',
        "Building Total GSF":
            '''
            What is the total gsf or total gross square footage (GSF) of development under the No-Action scenario specifically for all projected sites combined, as explicitly stated in a summary table or paragraph? It is also known as the maximum amount of floor area that can be developed in the zoning classification under No-Action Condition
            Ensure the value includes only the total GSF under the "No-Action" scenario. 
            When answering, use this format:
            Format: Building Total GSF (no action): [number]
            '''
    }]
}

rag_fusion_with_action = {
    "Project Description": [{
        "Affordable residential (low AMI - supportive)":
            ''' How many affordable residential units designated for low AMI (such as up to 80% of AMI) or supportive housing are included in the proposed action?. Look for the values in RWCDS Summary if the table is present.
            When answering, use this format:
            Format:
            Affordable residential (low AMI - supportive) With Action: [number]
            ''',
        "Office Space":
            '''What is the total square footage or Gross Floor Area of office or commercial space under the 'With Action' condition?
                - Prefer values explicitly labeled as "Commercial GSF," "Office GSF," or "Gross floor area (sq. ft.) under With Action."
                - Look for terms like "Development Site," "With Action Condition," or "Total GSF" nearby.
                - Ignore values under "No Action" or "Increment."
            When answering, use this format:
            Format:
            Total GSF With Action: [number]
            ''',
        "Healthcare facilities":
            '''
            How many square feet of space is designated exclusively for healthcare facilities, such as hospitals, clinics, or medical offices, explicitly mentioned under the WITH-ACTION CONDITION?
            When answering, use this format:
            Format: Healthcare facilities With Action: [number]
            ''',
        "Community Space":
            '''
            How many gross square feet (GSF) of Community Facility Space, including medical if available, is present under With Action Condition?
            When answering, use this format:
            Format: Community Space With Action: [number]
            ''',
        "Cultural Space":
            '''
            How many square feet of space is designated for cultural facilities explicitly mentioned under the WITH-ACTION CONDITION?
            When answering, use this format:
            Format: Cultural Space With Action: [number]
            ''',
        "Affordable Residential (high AMI)":
            '''
            How many units of affordable residential with AMI greater than or equal to 80% are proposed with action condition? Total Affordable Units- Affordable units earning upto 80% of AMI = Affordable Residential (high AMI). 
            When answering, use this format:
            Format: Affordable Residential (high AMI) With Action: [number]
            ''',
        "Parking Space":
            '''
            How many Parking Spaces are available With-Action condition on the development Site/Buildings? Look explicitly for values in tables summarizing parking availability or parking provision under the "With-Action" condition. Ignore values that represent total parking capacity in study areas or broader regions unless explicitly tied to the With-Action condition. For cases involving parking loss or displacement, subtract the number of spaces lost explicitly from any prior totals.
            When answering, use this format:
            Format:
            Parking Space With Action: [number]
            ''',
        "Market Rate Residential":
            '''What is the total number of occupied Dwelling Units (DU) present specifically under With‐Action Condition, in table mentioning Increment, for Residential Land Use? All values are explicitly in a table. This value is also known as Total Dwelling Units (DU) or approximately how many DUs?
            When answering, use this format:
            Format: Market Rate With Action: [number]
            ''',
        "Commercial Space":
            '''
            How many square feet of large commercial spaces are available with action condition? These are the spaces used for Cinema, Supermarket and Physical Culture Establishment etc. and not office, retail or other centers.
            When answering, use this format:
            Format: Commercial Space With Action: [number]
            ''',
        "Building Total GSF":
            '''
            What is the  total gsf or total gross square footage (GSF) of development under the With-Action scenario? Give the exact number. "
            When answering, use this format:
            Format: Building Total GSF (with action): [number]
            '''
    }]
}

rag_with_no_action = {
    "Open Space": [{
        "Open Space Ratio": '''
        "What is the open space ratio (OSR) or total open space available in the study area under the no action condition?" 
        When answering, use this format:
        Format: Open Space With No Action: [number]
        '''
    }]
}

rag_with_action = {
    "Socioeconomic": [{
        "Displacement Residential": '''
        "How many existing residential units will be displaced due to the proposed development?"
        When answering, use this format:
        Format: Displacement Residential With Action: [number]
        ''',
        
        "Displacement Commercial": '''
        "What is the total square footage of commercial spaces that will be displaced with the proposed actions?"
        When answering, use this format:
        Format: Displacement Commercial With Action: [number]
        ''',
        
        "Displacement Vacant": '''
        "How many vacant lots or properties will be displaced due to the proposed development?"
        Format: Displacement Vacant With Action: [number]
        '''
    }],
    "Open Space": [{
        "Open Space Ratio": '''
        "What is the open space ratio (OSR) of the study area resulting from with action condition?" When answering, use this format:
        Format: Open Space With Action: [number]
        '''
    }],
    
    "SolidWaste": [{
        "Solid Waste Generation": '''
        "How many tons of solid waste per week are expected to be generated by the proposed development under action?" When answering, use this format:
        Format: Solid Waste With Action: [number]
        '''
    }],
    
    "GreenHouse Gas": [{
        "Greenhouse Gas Emissions": '''
        "What is the estimated annual greenhouse gas emission in tons from building operations after the proposed development?" When answering, use this format:
        Format: Greenhouse Gas Emissions With Action: [number]
        '''
    }]
}


###############################################################################
# 6. UNIT LABELS
###############################################################################
component_units_map = {
    "Office Space": "SF",
    "Healthcare facilities": "SF",
    "Community Space": "SF",
    "Cultural Space": "SF",
    "Commercial Space": "GSF",
    "Building Total GSF": "SF",
    "Parking Space": "Spaces",
    "Market Rate Residential": "Units",
    "Affordable residential (low AMI - supportive)": "Units",
    "Affordable Residential (high AMI)": "Units",
    "Open Space Ratio": "Acre/Person",
    "Displacement Residential": "units",
    "Displacement Vacant": "SF",
    "Displacement Commercial": "Jobs",  
    "Solid Waste Generation": "weekly tons",
    "Greenhouse Gas Emissions": "annual tons",
}
