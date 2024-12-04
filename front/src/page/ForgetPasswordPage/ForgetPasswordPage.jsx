import { Link } from "react-router-dom"
import module from "./ForgetPasswordPage.module.css"

const ForgetPasswordPage = () => {
    return (
        <div>
            <Link to={"/login"}>Повернутися до логіну</Link>
            <div className={module.formDiv}>
                <input placeholder="Enter your email" className={module.formInput} />
                <button className={module.formBtn}>Відправити</button>
            </div>
        </div>
    )
}

export default ForgetPasswordPage