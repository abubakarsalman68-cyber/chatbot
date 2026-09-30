"use client";

import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import { ArrowUpIcon, AudioLinesIcon, SquareIcon, PaperclipIcon, XIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { APP_CONFIG } from "@/lib/config";
import { cn } from "@/lib/utils";

export function Composer({
  onSend,
  onStop,
  onVoice,
  streaming,
  disabled,
  placeholder = `Message ${APP_CONFIG.appName}…`,
  autoFocus,
}: {
  onSend: (text: string, attachments?: { url: string; type: "image" }[]) => void;
  onStop: () => void;
  /** When set, an empty composer shows a "Start voice mode" button instead of Send. */
  onVoice?: () => void;
  streaming: boolean;
  disabled?: boolean;
  placeholder?: string;
  autoFocus?: boolean;
}) {
  const [value, setValue] = useState("");
  const [attachments, setAttachments] = useState<{ url: string; type: "image" }[]>([]);
  const [uploading, setUploading] = useState(false);
  const ref = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && window.matchMedia("(min-width: 768px)").matches) ref.current?.focus();
  }, [autoFocus]);

  const submit = (e?: FormEvent) => {
    e?.preventDefault();
    if (streaming) return onStop();
    if ((!value.trim() && !attachments.length) || disabled) return;
    onSend(value, attachments);
    setValue("");
    setAttachments([]);
  };

  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    const touch = window.matchMedia("(hover: none)").matches;
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing && !touch) {
      e.preventDefault();
      submit();
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files?.length) return;

    setUploading(true);
    const formData = new FormData();

    const file = files[0];
    formData.append("file", file);

    try {
      const res = await fetch("/api/upload", { method: "POST", body: formData });
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      setAttachments((prev) => [...prev, { url: data.url, type: "image" }]);
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const removeAttachment = (url: string) => {
    setAttachments((prev) => prev.filter((a) => a.url !== url));
  };

  const canSend = streaming || ((!!value.trim() || attachments.length) && !disabled);
  const showVoice = !!onVoice && !streaming && !value.trim();

  return (
    <form
      onSubmit={submit}
      className="mx-auto w-full max-w-3xl rounded-3xl border bg-card p-2.5 pl-4 shadow-sm transition-colors focus-within:border-ring"
    >
      <label htmlFor="composer" className="sr-only">
        Message
      </label>
      <textarea
        id="composer"
        ref={ref}
        rows={1}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        enterKeyHint="send"
        className="field-sizing-content max-h-52 min-h-7 w-full resize-none bg-transparent py-1.5 text-[15px] leading-6 outline-none placeholder:text-muted-foreground"
      />
      {attachments.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {attachments.map((a) => (
            <div key={a.url} className="relative size-16 overflow-hidden rounded-lg border">
              <img src={a.url} alt="Upload preview" className="size-full object-cover" />
              <button
                type="button"
                onClick={() => removeAttachment(a.url)}
                className="absolute right-0.5 top-0.5 rounded-full bg-destructive p-0.5 text-destructive-foreground shadow-sm"
              >
                <XIcon className="size-3" />
              </button>
            </div>
          ))}
        </div>
      )}
      <div className="mt-1 flex items-center justify-end gap-2">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          className="hidden"
        />
        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading || disabled}
          aria-label="Upload image"
          className="text-muted-foreground hover:text-foreground"
        >
          <PaperclipIcon className={cn("size-4", uploading && "animate-spin")} />
        </Button>
        {showVoice ? (
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                type="button"
                size="icon"
                onClick={onVoice}
                aria-label="Start voice mode"
                className="rounded-full"
              >
                <AudioLinesIcon />
              </Button>
            </TooltipTrigger>
            <TooltipContent>Start voice mode</TooltipContent>
          </Tooltip>
        ) : (
          <Button
            type="submit"
            size="icon"
            disabled={!canSend}
            aria-label={streaming ? "Stop generating" : "Send message"}
            className={cn("rounded-full", !canSend && "opacity-30")}
          >
            {streaming ? <SquareIcon className="size-3.5 fill-current" /> : <ArrowUpIcon />}
          </Button>
        )}
      </div>
    </form>
  );
}
