from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from utils.PGSQLUtil import PGSQLUtil

import uvicorn
import json

pgsqlUtil = PGSQLUtil(host="127.0.0.1", user="yaokz", password="yaokz1314", database="myroot")

app = FastAPI()


@app.post("/receive/")
async def receive_message(
        type: str = Form(...),
        content: str = Form(...),
        source: str = Form(...),
        isMentioned: str = Form(...),
        isMsgFromSelf: str = Form(...),
):
    # 处理请求数据
    response_data = {
        "type": type,
        "content": content,
        "source": source,
        "isMentioned": isMentioned,
        "isMsgFromSelf": isMsgFromSelf,
    }

    print(response_data)

    try:
        # 群信息
        room_dict = json.loads(source).get("room")
        if room_dict != {}:
            # 群名
            print(room_dict['payload']['topic'])

        # 发送消息人信息
        from_dict = json.loads(source).get("from")
        if from_dict != {}:
            # 备注
            print(from_dict['payload']['alias'])
            # 昵称
            print(from_dict['payload']['name'])

        # 收消息人信息 （群聊没有）
        to_dict = json.loads(source).get("to")
        if to_dict != {}:
            print(to_dict['payload']['alias'])
            print(to_dict['payload']['name'])

        # 处理来自自己的消息
        if isMsgFromSelf:
            print("处理来自自己的消息")

        # @机器人的消息处理
        if isMentioned:
            print("@机器人的消息处理")
            if type == "text":
                content_tuple = content.split("@#")
                if len(content_tuple) < 2:
                    # 流水处理
                    journal_data_insert(content_tuple[0], content_tuple[1])
                else:
                    print("格式错误")
        else:
            print("不处理")

        # 填写处理逻辑-开始
        if type == "text":
            print("文本信息")
        elif type == "urlLink":
            print("链接卡片")
        elif type == "file":
            print("文件")
        elif type == "friendship":
            print("还有请求")
        elif type == "system_event_login":
            print("登陆")
        elif type == "system_event_logout":
            print("登出")
        elif type == "system_event_error":
            print("异常报错")
        elif type == "system_event_push_notify":
            print("快捷回复后消息推送状态通知")
        else:
            print("unknown")

        # 填写处理逻辑-结束
        return JSONResponse(content={"status": "success", "data": response_data})
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "error", "data": "处理失败"})


def journal_data_insert(wx_id, money):
    sql = 'insert into journal (wx_id, money) values (%s, %s)'%wx_id,money
    pgsqlUtil.execute(sql)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
