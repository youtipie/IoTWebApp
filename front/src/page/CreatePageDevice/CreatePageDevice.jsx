import module from "./CreatePageDevice.module.css"

import { Formik, Form, Field, ErrorMessage } from 'formik';
import { Link } from "react-router-dom";
import * as Yup from 'yup';

const CreatePageDevice = () => {
    const INITIAL_VALUES = {
        state: '',
        type: '',
        isOn: ''
    };

    const validationSchema = Yup.object({
        state: Yup.string().required("Стан є обов'язковим полем"),
        type: Yup.string().required("Тип є обов'язковим полем"),
        isOn: Yup.string().required("Виберіть, чи девайс увімкнений")
    });

    const handleSubmit = (values, actions) => {
        console.log(values);
        actions.resetForm();
    };

    return (
        <div className={module.createDiv}>
            <Link className={module.goBackLick} to={"/"}>Повернутися на головну</Link>
            <h1>Підключити девайс</h1>
            <Formik
                initialValues={INITIAL_VALUES}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >
                <Form className={module.form}>
                    <label className={module.formLabel}>
                        Введіть стан:
                        <Field type="text" name="state" />
                        <ErrorMessage name="state" component="span" />
                    </label>
                    <label className={module.formLabel}>
                        Введіть тип:
                        <Field type="text" name="type" />
                        <ErrorMessage name="type" component="span" />
                    </label>
                    <fieldset>
                        <legend>Девайс увімкнений:</legend>
                        <label>
                            <Field type="radio" name="isOn" value="true" />
                            Так
                        </label>
                        <label>
                            <Field type="radio" name="isOn" value="false" />
                            Ні
                        </label>
                        <ErrorMessage name="isOn" component="span" />
                    </fieldset>
                    <button type="submit">Створити девайс</button>
                </Form>
            </Formik>
        </div>
    );
};

export default CreatePageDevice;

