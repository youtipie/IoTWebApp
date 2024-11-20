import module from "./RegistrationPage.module.css";

import { Formik, Form, Field, ErrorMessage } from "formik";
import { Link } from "react-router-dom";
import * as Yup from "yup";
import { useDispatch, useSelector } from "react-redux";
import { register } from "../../redux/auth/operations";
import { selectError, selectIsLoading } from "../../redux/auth/selectors";

const RegistrationPage = () => {
    const dispatch = useDispatch();
    const isLoading = useSelector(selectIsLoading);
    const error = useSelector(selectError);

    const INITIAL_VALUES = {
        username: "",
        email: "",
        password: "",
    };

    const validationSchema = Yup.object({
        username: Yup.string()
            .min(3, "Ім'я користувача має містити щонайменше 3 символи")
            .required("Ім'я користувача є обов'язковим полем"),
        email: Yup.string()
            .email("Неправильний формат електронної пошти")
            .required("Електронна пошта є обов'язковим полем"),
        password: Yup.string()
            .min(6, "Пароль повинен бути не менше 6 символів")
            .required("Пароль є обов'язковим полем"),
    });

    const handleSubmit = (values, actions) => {
        dispatch(register(values));
        actions.resetForm();
    };

    return (
        <div className={module.formDiv}>
            <h1>Реєстрація</h1>
            <Formik
                initialValues={INITIAL_VALUES}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                <Form className={module.form}>
                    <label className={module.formLabel}>
                        Імя користувача:
                        <Field type="text" name="username" />
                        <ErrorMessage name="username" component="span" />
                    </label>
                    <label className={module.formLabel}>
                        Електронна пошта:
                        <Field type="email" name="email" />
                        <ErrorMessage name="email" component="span" />
                    </label>
                    <label className={module.formLabel}>
                        Пароль:
                        <Field type="password" name="password" />
                        <ErrorMessage name="password" component="span" />
                    </label>

                    {error && <p className={module.errorMessage}>{error}</p>}
                    {isLoading ? (
                        <p>Завантаження...</p>
                    ) : (
                        <button type="submit">Зареєструватися</button>
                    )}
                </Form>
            </Formik>
            <Link to={"/login"} className={module.link}>
                Вже маєте акаунт?
            </Link>
        </div>
    );
};

export default RegistrationPage;

