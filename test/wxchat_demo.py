from wxauto import *

# 获取当前微信客户端
wx = WeChat()

# 获取好友信息
friends = wx.GetFriends()
for friend in friends:
    print(f"好友昵称: {friend['NickName']}, 备注: {friend['RemarkName']}")

# 获取群组信息
groups = wx.GetGroups()
for group in groups:
    print(f"群组名称: {group['NickName']}, 成员数量: {group['MemberCount']}")