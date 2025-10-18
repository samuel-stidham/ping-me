import { useState } from "react";
import { View, Text, TextInput, Button, ActivityIndicator, Alert } from "react-native";
import Constants from "expo-constants";

const API_BASE =
  (Constants?.expoConfig?.extra as any)?.API_BASE ||
  process.env.EXPO_PUBLIC_API_BASE ||
  "http://192.168.1.200:5001"; // keep in sync with app.json for your LAN IP

export default function PingMe() {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "ok" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const send = async () => {
    const trimmed = message.trim();
    if (!trimmed) {
      setError("Message cannot be empty.");
      return;
    }
    // mirror server rule: hard-cap at 160 chars
    const body = trimmed.length > 160 ? trimmed.slice(0, 160) : trimmed;

    setError(null);
    setStatus("sending");
    try {
      const res = await fetch(`${API_BASE}/send-ping`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message_body: body }),
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok || data?.status !== "success") {
        throw new Error(data?.message || `HTTP ${res.status}`);
      }

      setStatus("ok");
      setMessage("");
      Alert.alert("Sent ✅", "SMS successfully queued by Twilio.");
    } catch (e: any) {
      setStatus("error");
      const msg = e?.message || "Failed to send.";
      setError(msg);
      Alert.alert("Send failed ❌", msg);
    } finally {
      setTimeout(() => setStatus("idle"), 1200);
    }
  };

  return (
    <View style={{ flex: 1, padding: 16, gap: 12, justifyContent: "center" }}>
      <Text style={{ fontSize: 22, fontWeight: "600" }}>Ping Me 📲</Text>

      <TextInput
        value={message}
        onChangeText={setMessage}
        placeholder="Type a message to yourself…"
        placeholderTextColor="#aaa"
        style={{
            borderWidth: 1,
            borderRadius: 8,
            padding: 12,
            borderColor: "#ccc",
            backgroundColor: "#fff",   // make box white
            color: "#000"              // make text black
        }}
        maxLength={200}
      />

      {status === "sending" ? (
        <ActivityIndicator size="large" />
      ) : (
        <Button title="Send" onPress={send} />
      )}

      {error && <Text style={{ color: "red" }}>{error}</Text>}
      {status === "ok" && <Text style={{ color: "green" }}>Sent!</Text>}

      <Text style={{ color: "#666", marginTop: 8 }}>API: {API_BASE}</Text>
    </View>
  );
}
