import React, { Component } from 'react';
import DropdownQuestion from './DropdownQuestion';
import Input from './Input';


class SymptomPredictionModel extends Component{
    constructor(props){
        super(props);
        this.state = {
            isLoading : true,
            questionList: false,
            values: {},
            covidRisk: 0.0
        };

        fetch("./symptom_prediction_model_questions")
        .then(
            (response) => {
                return response.json();
            }
        )
        .then(
            (data) => {
                this.setState({questionList : data.questions});
                let defaultValues = {}
                data.questions.map((question) =>{
                    defaultValues[question.name] = question.default;
                })
                this.setState({values : defaultValues})
                return {}
            }
        )
        .then(
            (data) => {
                this.setState({isLoading : false})
            }
        )
        .catch(console.log);
    }


    updateValue(key, value){
        let tempValues = this.state.values;
        tempValues[key] = value;
        this.setState({values: tempValues})
        this.calculate();
    }

    calculate(){
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.state.values)
        }

        fetch("./symptom_prediction_model_result", requestOptions)
        .then(
            (response) => {
                return response.json();
            }
        )
        .then(
            (data) => {
                this.setState({covidRisk : data.result})
                this.props.updateCovidValue(this.state.covidRisk)
            }
        )
        .catch(console.log)
    }



    render(){

        if(this.state.isLoading === true){
            return(
                <h3>
                    ... Loading ...
                </h3>
            )
        }


        return (
            <div>
                <h1>
                    Individual COVID Risk Calculator
                </h1>
                {this.state.questionList.map(
                    (question, i) => {
                        if(question.question_type === 'dropdown'){
                            return (
                                <DropdownQuestion   key={i}
                                                    updateValue={this.updateValue.bind(this)}
                                                    title={question.title}
                                                    choices={question.choices}
                                                    name={question.name}/>
                            )
                        }
                        if(question.question_type === 'input'){
                            return (
                                <Input              key={i}
                                                    title={question.title}
                                                    updateValue={this.updateValue.bind(this)}
                                                    name={question.name}
                                />
                            )
                        }
                    }
                )}
            </div>
        )
    }

}

export default SymptomPredictionModel;
