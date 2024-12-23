const imageDimension = 200;
const mean = [0.485, 0.456, 0.406];
const std = [0.229, 0.224, 0.225];

gender_mapping = {0: 'Female', 1: 'Male'}
ethnicity_mapping = {0: 'Asian', 1: 'Black', 2: 'Indian', 3: 'Others', 4: 'White'}
emotion_mapping = {0: 'Anger', 1: 'Contempt', 2: 'Disgust', 3: 'Fear', 4: 'Happy', 5: 'Neutral', 6: 'Sad', 7: 'Surprise'}
idx_to_age_range = {0: '0-2', 1: '3-9', 2: '10-19', 3: '20-24', 4: '25-29', 5: '30-34', 6: '35-39', 7: '40-44', 8: '45-54', 9: '55-116'}

function model_path(my_feature){
    model_folder = "/static/tfjs_models"
    if (my_feature == "gender") {
        return `${model_folder}/gender_model_js/model.json`
    }
    else if (my_feature == "ethnicity") {
        return `${model_folder}/ethnicity_model_js/model.json`        
    }
    else if (my_feature == "emotion"){
        return `${model_folder}/emotion_model_js/model.json`
    }
    else if (my_feature == "age_range"){
        return `${model_folder}/age_range_model_js/model.json`
    }
    else{
        return `${model_folder}/age_model_js/model.json`
    }
}

function find_value_by_logit(logit, my_feature){
    if (my_feature == "gender") {
        let gender_id = (1 / (1 + Math.exp(-logit[0])) > 0.5) ? 1 : 0;
        return gender_mapping[gender_id]; 
    }

    else if (my_feature == "ethnicity") {
        const ethnicity_id = Object.values(logit).indexOf(Math.max(...Object.values(logit)));  
        return ethnicity_mapping[ethnicity_id]; 
    }

    else if (my_feature == "emotion"){
        const emotion_id = Object.values(logit).indexOf(Math.max(...Object.values(logit)));  
        return emotion_mapping[emotion_id]; 
    }
    
    else if (my_feature == "age_range"){
        const age_label = Object.values(logit).indexOf(Math.max(...Object.values(logit)));  
        return age_range = idx_to_age_range[age_label];  
    }
    else{
        return Math.round(logit[0]);
    }
}