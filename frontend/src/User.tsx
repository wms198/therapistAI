import { UserMessage } from "./types";

interface Props {
    messages: UserMessage;
}

const User = ({messages}: Props) => {
    const handleSubmit = (e: React.SyntheticEvent) => {
        e.preventDefault();
        const target = e.target as typeof e.target & {
                textArea: { value: string };
                }
        const textArea = target.textArea.value;
        console.log(textArea)
    }

    return(
        <div className="py-3 mx-auto row" style={{ width: "50%" }}>
        <div className="col align-self-center">
        <p className="lead text-center" id="therapist">Hi. I'm here.</p>
        {/* <div className="input-group position-relative"> */}
        <div className="d-flex flex-column">
            <form onSubmit={handleSubmit} >
            <textarea
                className="form-control custom-control"
                rows={4}
                cols={72}
                id='textArea'
            >
            </textarea>
            <button
                className="btn btn-primary"
                style={{ width: "100%", marginTop: "24px" }}
            >
                send
            </button>
            </form>
            {/* <div className="position-absolute d-flex justify-content-end fixed-bottom">
            <button  className="btn btn-primary" style={{width: '100%'}} >↑</button>
        </div> */}
        </div>
        </div>
    </div>
    );
}

export default User;