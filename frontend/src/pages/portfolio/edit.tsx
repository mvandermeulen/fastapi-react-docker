import { useForm, Form, Input, Select, Edit, useSelect, RefreshButton, ListButton } from "@pankod/refine-antd";
import { IBroker, IPortfolio } from "interfaces";
import { HttpError } from "@pankod/refine-core";
import { Space } from "antd";
import React from "react";

export const PortfolioEdit: React.FC = () => {
    const { formProps, saveButtonProps, queryResult } = useForm<IPortfolio,
        HttpError,
        IPortfolio>({
        metaData:{
            fields: [
                "id",
                "name",
                "brokerId"
            ],
        },
    });

    const postData = queryResult?.data?.data;

    const { selectProps: brokerSelectProps } = useSelect<IBroker>({
        resource: "brokers",
        metaData:{
            fields: [
                "id",
                "name",
            ],
        },
        optionLabel: "name",
        optionValue: "id",
        defaultValue: postData?.brokerId
    });



    return (
        <Edit saveButtonProps={saveButtonProps}
              pageHeaderProps={{ extra:
                  <Space wrap>
                      <ListButton />
                      <RefreshButton
                          onClick={() =>{
                              if(postData)  // hack to fire rerender
                                postData.name=''
                              queryResult?.refetch()
                          }}
                      />
                  </Space> }}
        >
            <Form {...formProps} layout="vertical">
                <Form.Item label="Name" name="name"
                           rules={[
                    {
                        required: true,
                    },
                ]}>
                    <Input />
                </Form.Item>
                <Form.Item label="Broker" name="brokerId">
                    <Select {...brokerSelectProps} />
                </Form.Item>
            </Form>
        </Edit>
    );
}