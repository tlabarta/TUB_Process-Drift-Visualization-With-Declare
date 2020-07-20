import React, { useState, useContext } from "react";
import { Upload, Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";

import { uploadFile } from "../../apiService";
import { AppContext, SET_SESSION_ACTION } from "../../context/appContext";
import './Upload.css';

export const UploadComponent = () => {
  const { dispatch, state } = useContext(AppContext);
  const [loading, setLoading] = useState<boolean>(false);

  if (state.session_id) {
    return null
  }


  const handleSubmitForm = async ({
    file,
    onSuccess,
    onError,
  }: {
    file: File;
    onSuccess: (response: object, file: File) => void;
    onError: (event: Error, body?: Object) => void;
  }) => {
    if (file) {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);
      try {
        const response = await uploadFile(formData);
        dispatch({ type: SET_SESSION_ACTION, payload: response });
        onSuccess(response, file);
      } catch (error) {
        console.log(error);
        onError(error);
      }
      setLoading(false);
    }
  };

  return (
    <Upload
      className="Upload-button"
      accept=".xes"
      name="file"
      customRequest={handleSubmitForm}
    >
      <Button loading={loading}>
        <UploadOutlined /> Click to Upload
      </Button>
    </Upload>
  );
};