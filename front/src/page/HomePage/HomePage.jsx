import { Link } from "react-router-dom";

const HomePage = () => {
    return (
        <div>
            <Link to={'/networks'}>Network</Link>
        </div>
    );

};

export default HomePage;
