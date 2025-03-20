from mycelery.main import app
from skylark_api.libs.tencent.sms import TencentSMS
import logging

log = logging.getLogger("django")


@app.task(name="send_sms")
def send_sms(mobile, sms_code):
    """发送短信"""
    try:
        # 腾讯云发送短信验证码
        tencent_send_sms = TencentSMS()
        result = tencent_send_sms.send_sms(phone_number=mobile, template_param_set=sms_code)
        print(result)
        if not result:
            log.error(f"短信发送失败！手机号：{mobile}")
    except Exception as e:
        log.error(f"短信发送异常：{e}")
