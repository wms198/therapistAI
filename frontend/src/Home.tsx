import { Link } from "react-router";

const Home: React.FC = () => {


    return (
        <div className="d-flex flex-column align-items-center justify-content-center">
            <div>
                Hello. Before start our conversation.
            </div>
            <div>
                Please sign up with your google account.
                    <span><Link
                        to={
                            `https://accounts.google.com/o/oauth2/auth?client_id=${process.env.REACT_APP_GOOGLE_OAUTH_CLIENT_ID}&redirect_uri=${process.env.REACT_APP_GOOGLE_REDIRECT_URI}&scope=openid&response_type=code`
                        }>
                            <img src="./google-logo-icon.png" alt="google icon" />
                    </ Link></span>
            </div>
        </div>
    );
}

export default Home;