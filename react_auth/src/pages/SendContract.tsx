import { SyntheticEvent, useEffect, useState } from "react";

const SendContract = (props:{name: string, setName: (name:string)=>void, id: string, setId: (id:string)=>void, user_type:string}) => {
    const [hotelijerMessage, setHotelijerMessage] = useState("");
    const [withdrawCondition, setWithdrawCondition] = useState("");
    const [percentage, setPercentage] = useState("");

    const sendContract = async (e:SyntheticEvent) => {
        e.preventDefault();

        const hotelijerId = parseInt(props.id);
        const hotelijerName = props.name
        const response = await fetch(`http://localhost:8000/api/create-contract`,{
            method:"POST",
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({hotelijerId, hotelijerName, hotelijerMessage, withdrawCondition, percentage})
        });

        if (response.ok){
            const data = await response.json();
            console.log(data);
        }else{
            console.log('Error')
        }
    }

    let menu;

    if (props.user_type === 'Hotelijer'){
        menu = (<> <h1>Contracts Form</h1>
    <div className="container">
        <div className="form-f form">
            <form>
                <h1 className="h3 mb-3 font-weight-normal">Create contract</h1>
                <input type="text" name="hotelijerMessage" className="form-control" placeholder="Message... "  onChange={(e)=>{setHotelijerMessage(e.target.value)}} required />
                <input type="text" name="withdrawCondition" className="form-control" placeholder="Withdraw Condition... " onChange={(e)=>{
                        setWithdrawCondition(e.target.value)
                }}   required/>
                <input type="number" name="percentage" className="form-control" placeholder="Percentage... " onChange={(e)=>{
                        setPercentage(e.target.value)
                }}required/>
            </form> 
             <button className="btn btn-lg btn-primary btn-block" type="submit" onClick={(e)=>{sendContract(e)}}>Send contract</button>
        </div>
    </div></>)
    }else{
        menu = <div className="container"><h1>Access Denied</h1></div>
    }

    return ( <>
       {menu}
    </> );
}
 
export default SendContract;