import module from "./RegistrationPage.module.css"

import { Formik, Form, Field, ErrorMessage } from 'formik';
import { Link } from "react-router-dom";
import * as Yup from 'yup';

const RegistrationPage = () => {
    const INITIAL_VALUES = {
        email: '',
        password: '',
        confirmPassword: '',
    };

    const validationSchema = Yup.object({
        email: Yup.string()
            .email("Неправильний формат електронної пошти")
            .required("Електронна пошта є обов'язковим полем"),
        password: Yup.string()
            .min(6, "Пароль повинен бути не менше 6 символів")
            .required("Пароль є обов'язковим полем"),
        confirmPassword: Yup.string()
            .oneOf([Yup.ref('password'), null], "Паролі не співпадають")
            .required("Підтвердження пароля є обов'язковим полем"),
    });

    const handleSubmit = (values, actions) => {
        console.log(values);
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
                        Електронна пошта:
                        <Field type="email" name="email" />
                        <ErrorMessage name="email" component="span" />
                    </label>
                    <label className={module.formLabel}>
                        Пароль:
                        <Field type="password" name="password" />
                        <ErrorMessage name="password" component="span" />
                    </label>
                    <label className={module.formLabel}>
                        Підтвердження пароля:
                        <Field type="password" name="confirmPassword" />
                        <ErrorMessage name="confirmPassword" component="span" />
                    </label>
                    <Link to={"/login"}>Вже маєте акаунт?</Link>
                    <button type="submit">Зареєструватися</button>
                </Form>
            </Formik>
        </div>
    );
};

export default RegistrationPage;
