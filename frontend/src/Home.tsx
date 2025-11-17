import { Image } from "react-bootstrap";
import { Link } from "react-router";
import googleIcon from "./assets/google-logo-icon.png";

const Home: React.FC = () => {


    return (
        <div className="d-flex flex-column align-items-center justify-content-center">
            <div>
                Hello. Before start our conversation.
            </div>
            <div>
                Please sign up with your google account.
                    {/* https://stackoverflow.com/a/51533282 */}
                    <span><Link
                        to={
                            `https://accounts.google.com/o/oauth2/auth?client_id=${process.env.REACT_APP_GOOGLE_OAUTH_CLIENT_ID}&redirect_uri=${process.env.REACT_APP_GOOGLE_REDIRECT_URI}&scope=openid&response_type=code`
                        }>
                        <Image src={googleIcon} alt="google icon" className="image-logo-size"/>
                    </ Link></span>
            </div>
        </div>
    );
}

export default Home;