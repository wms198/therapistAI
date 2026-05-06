import { Image } from 'react-bootstrap';
import { Link } from 'react-router';
import googleIcon from '../assets/google-logo-icon.png';
import SignIn from './SignIn'

const Home: React.FC = () => {
    //return (<>foooo</>)
    return (
        <div className="d-flex flex-column align-items-center justify-content-center">
            <div>
                <SignIn />
            </div>
            <div>
                Hello. Before start our conversation.
            </div>
            <div>
                Please sign up with your google account.
                    {/* https://stackoverflow.com/a/51533282 */}
                    <span><Link
                        to={
                            `https://accounts.google.com/o/oauth2/auth?client_id=${import.meta.env.GOOGLE_OAUTH_CLIENT_ID}&redirect_uri=${import.meta.env.GOOGLE_REDIRECT_URI}&scope=openid&response_type=code`
                        }>
                        <Image src={googleIcon} alt="google icon" className="image-logo-size"/>
                    </ Link></span>
            </div>
        </div>
    );
}

export default Home;